from setuptools import find_packages, setup

setup(
    name='netbox-cloud-plugin',
    version='1.1',
    description='NS1 NetBox Cloud',
    url='https://github.com/nsone/netbox-cloud-plugin',
    author='NS1',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
