FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-devel

ENV DEBIAN_FRONTEND=noninteractive

# Remove any third-party apt sources to avoid issues with expiring keys.
RUN rm -f /etc/apt/sources.list.d/*.list

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
    && apt-get install -y unzip curl sox && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $USERNAME

RUN mkdir -p /home/${USERNAME}/sgevc
WORKDIR /home/${USERNAME}/sgevc

# Copy requirements.txt and install Python dependencies
COPY --chown=$USERNAME:$USERNAME requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=$USERNAME:$USERNAME . .

# Compile monotonic_align (TODO: not sure if I need to do this manually)
# WORKDIR /home/${USERNAME}/sgevc/monotonic_align
# RUN python setup.py build_ext --inplace

# CMD ["/bin/bash", "-c", "while sleep 1000; do :; done"]
CMD ["python", "train.py", "-c", "configs/ESD_base_en.json", "-m", "ESD_english_semi_3_gamma_1.0_alpha_0.2"]