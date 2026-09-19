FROM rust:1.88-alpine as rust-builder
#minify html+js+css in my frontend page

RUN apk update
RUN apk add --no-cache musl-dev

WORKDIR /build

COPY Cargo.toml .
COPY main.rs ./src/main.rs
RUN cargo build --release

#generate basic auth password
RUN apk add apache2-utils

RUN mkdir -p /build/secrets
#if don't want to use secrets
# ARG ADMIN_PASSWORD=defaultValue
# RUN htpasswd -bB -c /build/secrets/.htpasswd admin "$ADMIN_PASSWORD"
RUN --mount=type=secret,id=admin_password htpasswd -iB -c /build/secrets/.htpasswd admin < /run/secrets/admin_password

COPY index.html /build/index.html

RUN mkdir -p /build/minify
RUN /build/target/release/html-minifier-tool /build/index.html /build/minify/index.html

FROM nginx:1.31.5-alpine as production

COPY --from=rust-builder /build/minify/index.html /usr/share/nginx/html/index.html
COPY --from=rust-builder /build/secrets/.htpasswd /etc/nginx/secrets/.htpasswd
COPY nginx.conf /etc/nginx/nginx.conf