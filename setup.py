from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


install_requires = ["geopandas==0.10.2", "requests== 2.27.1"]

setup(
    name="ons_geoportal",
    version="0.1",
    description="Python tools for downloading geospatial vector data from \
    the Open Geography Portal",
    long_description=(readme()),
    long_description_content_type="text/markdown",
    url="https://github.com/tastatham/ons_geoportal",
    author="Thomas Statham",
    author_email="tastatham@gmail.com",
    keywords="download open geography portal, data, geopandas",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    include_package_data=False,
)
