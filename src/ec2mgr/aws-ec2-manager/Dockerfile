FROM python:3.12-slim

# prevent python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# prevent python buffering logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# copy project files
COPY pyproject.toml .
COPY src ./src

# install project
RUN pip install --no-cache-dir -e .

# default command
ENTRYPOINT ["ec2mgr"]
