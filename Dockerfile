FROM ubuntu:20.04

# ---------- 基础配置 ----------
ARG USERNAME=ubuntu
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# 国内源
RUN sed -i "s@http://.*archive.ubuntu.com@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list && \
    sed -i "s@http://.*security.ubuntu.com@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list

# ---------- 用户 ----------
RUN useradd -m -s /bin/bash ${USERNAME} \
 && usermod -aG sudo ${USERNAME} \
 && echo "${USERNAME}:${USERNAME}" | chpasswd

# ---------- Locale ----------
RUN apt-get update \
 && apt-get install -y locales tzdata \
 && locale-gen en_US.UTF-8 \
 && ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
 && echo $TZ > /etc/timezone \
 && dpkg-reconfigure -f noninteractive tzdata \
 && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8

# ---------- 系统依赖 ----------
RUN apt-get update && apt-get install -y \
    git \
    openssh-client \
    gcc \
    ca-certificates \
    curl \
    ssh \
    sudo \
    pkg-config \
    python3 \
    python3-venv \
    python3-pip \
    python3-dev \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libldap2-dev \
    libsasl2-dev \
    libmagic1 \
    libmysqlclient-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libpng-dev \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# ---------- Git 信息 ----------
RUN git config --system user.email "lk_ernest@163.com" \
 && git config --system user.name "kang"

# ---------- 切用户 ----------
USER ${USERNAME}

# ---------- SSH ----------
RUN mkdir -p /home/${USERNAME}/.ssh \
 && chmod 700 /home/${USERNAME}/.ssh \
 && ssh-keyscan -t ed25519 gitee.com >> /home/${USERNAME}/.ssh/known_hosts \
 && chmod 600 /home/${USERNAME}/.ssh/known_hosts

# ---------- pip 国内源（给 uv pip 用） ----------
RUN mkdir -p /home/${USERNAME}/.pip \
 && echo "[global]" > /home/${USERNAME}/.pip/pip.conf \
 && echo "index-url = https://repo.huaweicloud.com/repository/pypi/simple" >> /home/${USERNAME}/.pip/pip.conf \
 && echo "trusted-host = repo.huaweicloud.com" >> /home/${USERNAME}/.pip/pip.conf


ENV VIRTUAL_ENV=/home/${USERNAME}/liang_ba/.venv
ENV PATH="/home/${USERNAME}/.local/bin:$VIRTUAL_ENV/bin:$PATH"

# ---------- 工作目录 ----------
WORKDIR /home/${USERNAME}/liang_ba

# 复制依赖文件并安装
COPY --chown=${USERNAME}:${USERNAME} . .

# ---------- venv ----------
RUN pip3 install uv toml

# ---------- 示例：如果你需要 git clone / pip install 私有仓库 ----------
# RUN --mount=type=ssh \
#     pip install git+ssh://git@git.vbio.top/xxx/yyy.git

CMD ["bash"]
