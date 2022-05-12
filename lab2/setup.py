from setuptools import setup, find_packages


setup(
    name="serializer",
    version="1.0.0",
    description="Library for serialization JSON, YAML, TOML",
    author="Karina Krishtafovich",
    author_email="karina.krishtafovich@email.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["yaml", "toml"]
)
