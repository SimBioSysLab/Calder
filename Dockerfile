FROM continuumio/miniconda3

LABEL maintainer="Si <meditates@gmail.com>"

# Install useful tools
RUN conda install -y mamba -n base -c conda-forge && \
    mamba install -y python=3.9 pandas=1.4.4 seaborn scikit-learn -c conda-forge && \
    conda clean -afy
# Activate environment by default
SHELL ["conda", "run", "-n", "calder", "/bin/bash", "-c"]

# Create work directory
WORKDIR /Calder

# Copy repo contents
COPY . /Calder

