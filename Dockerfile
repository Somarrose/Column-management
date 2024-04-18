FROM python:3.10.12-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
# USER appuser

# Install application into container
COPY . .
# COPY entrypoint.sh /home/appuser

# Define environment variable
ENV FLASK_APP=app.py

# Initialize the database
# USER root
RUN chmod u+x /home/appuser/entrypoint.sh
# USER appuser

# Run app.py when the container launches
ENTRYPOINT ["./entrypoint.sh"]
