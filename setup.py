# setup.py
import codecs
with codecs.open('build.py', 'r') as build_file:
    build_source = build_file.read()
source = dict()
exec(build_source, source)
setup = source['setup']
def main() -> None:
    """Runs the function to distribute the package."""
    setup(
        package="auto_fastapi",
        exclude=[
            "__pycache__",
            "*.pyc"
        ],
        include=[],
        requirements="requirements.txt",
        dev_requirements="requirements-dev.txt",
        name='auto-fastapi',
        version='0.0.1',
        description=(
            "A pythonic functional way to construct FastAPI "
            "applications be declaring endpoints in separation "
            "of their functional definition, enabeling to separate, "
            "replicate, and reuse functions in different APIs at the "
            "same time, and also run multiple of them."
        ),
        license='MIT',
        author="Shahaf Frank-Shapir",
        author_email='shahaffrs@gmail.com',
        url='https://github.com/Shahaf-F-S/auto-fastapi',
        long_description_content_type="text/markdown",
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Operating System :: OS Independent"
        ]
    )
if __name__ == "__main__":
    main()
