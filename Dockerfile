FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

ARG USERNAME=containeruser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID --create-home $USERNAME --shell /bin/bash \
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    # Install libraries and development tools
    && apt-get install -y software-properties-common build-essential libtool autoconf unzip sox curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python and pip
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && \
    apt-get install -y python3-dev python3.9-distutils python3.9-dev python3.9 && \
    apt-get clean && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 && \
    curl https://bootstrap.pypa.io/get-pip.py | python3.9
# Set Python 3.9 as the default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

RUN mkdir -p /home/${USERNAME}/sgevc
WORKDIR /home/${USERNAME}/sgevc

COPY --chown=$USERNAME:$USERNAME . .

USER $USERNAME

CMD ["/bin/bash", "-c", "while sleep 1000; do :; done"]