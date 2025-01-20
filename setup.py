from setuptools import setup, find_packages

setup(
    name="mkdocs-bi-directional-links",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mkdocs>=1.0",
    ],
    entry_points={
        "mkdocs.plugins": [
            "bi-directional-links = mkdocs_bi_directional_links.plugin:BiDirectionalLinksPlugin",
        ],
    },
)