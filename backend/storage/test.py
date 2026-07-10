from storage.provider import MinIOProvider

provider = MinIOProvider()
print(provider.health_check())
print(provider.bucket_exists())