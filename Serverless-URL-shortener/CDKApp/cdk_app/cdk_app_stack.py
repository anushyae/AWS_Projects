from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_kms as kms,
    aws_secretsmanager as secretsmanager,
    aws_ec2 as ec2,
    aws_iam as iam,
    Tags,
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ✅ KMS Key (used for S3, DynamoDB)
        kms_key = kms.Key(self, "UrlShortenerKey",
            enable_key_rotation=True,
            alias="alias/url-shortener-key"
        )
        # ✅ S3 Bucket (for storing long URLs)
        s3_bucket = s3.Bucket(self, "UrlShortenerBucket",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms_key,
            removal_policy=RemovalPolicy.DESTROY,  # Only for dev/test environments
            auto_delete_objects=True,  # Only for dev/test environments
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )
        # ✅ VPC (for Lambda functions)
        vpc = ec2.Vpc(self, "UrlShortenerVPC",
            max_azs=2,  # Default is all AZs in the region
            nat_gateways=1,  # Use a single NAT gateway for cost efficiency
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                )
            ]
        )
        # ✅ Secrets Manager (for storing sensitive data)
        secret = secretsmanager.Secret(self, "UrlShortenerSecret",
            secret_name="UrlShortenerSecret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                exclude_punctuation=True,
                include_space=False,
                password_length=16
            )
        )
        # ✅ IAM Role (for Lambda functions)
        lambda_role = iam.Role(self, "UrlShortenerLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole")
            ]
        )
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:Scan"],
                resources=[table.table_arn]  # Replace with specific resource ARNs in production
            )
        )

        # The code that defines your stack goes here
        table = dynamodb.Table(
            self, "UrlTable",
            partition_key=dynamodb.Attribute(name="shortcode", type=dynamodb.AttributeType.STRING),
            billing_mode = dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy = dynamodb.RemovalPolicy.DESTROY
        )
        shortenUrl_fn = _lambda.Function(
            self, "ShortenUrlFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="shorten.handler",
            role=lambda_role,
            vpc=vpc,
            timeout=Duration.seconds(30),
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name,
                "S3_BUCKET": s3_bucket.bucket_name,
                "KMS_KEY_ID": kms_key.key_id,
                "SECRET_ARN": secret.secret_arn
                }
        )
        redirectUrl_fn = _lambda.Function(
            self, "RedirectUrlFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="redirect.handler",
            role=lambda_role,
            vpc=vpc,
            timeout=Duration.seconds(30),
            code=_lambda.Code.from_asset("lambda"),
            environment={"TABLE_NAME": table.table_name}
        )
        #Permisssions
        table.grant_read_data(redirectUrl_fn)
        table.grant_write_data(shortenUrl_fn)
        s3_bucket.grant_read(shortenUrl_fn)
        kms_key.grant_encrypt_decrypt(shortenUrl_fn)






    
        # example resource
        # queue = sqs.Queue(
        #     self, "CdkAppQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
