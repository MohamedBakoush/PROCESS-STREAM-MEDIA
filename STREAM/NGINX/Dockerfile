FROM ubuntu:latest 

# Create app directory
WORKDIR /stream/nginx

# Bundle app source
COPY . .

# Update and install necessary packages
RUN apt-get update && \
    apt-get -y install build-essential libpcre3 libpcre3-dev libssl-dev zlib1g zlib1g-dev wget

# Get nginx
RUN wget https://nginx.org/download/nginx-1.24.0.tar.gz && \
    tar -xf nginx-1.24.0.tar.gz && \
    rm nginx-1.24.0.tar.gz

# Redirect to nginx-1.24.0 directory
WORKDIR /stream/nginx/nginx-1.24.0

# Configure and build nginx
RUN ./configure --with-http_ssl_module --with-http_mp4_module && \
    make && \
    make install

# Redirect to home directory
WORKDIR /

# Replace nginx.conf (Make sure you have a valid nginx.conf in your app source)
RUN rm /usr/local/nginx/conf/nginx.conf && \
    mv /stream/nginx/nginx.conf /usr/local/nginx/conf/nginx.conf

# Create directory for videos
RUN mkdir -p /var/www/html/media

# Chown directory
RUN chown -R www-data:www-data /var/www/html/media

# Expose ports  
EXPOSE 433

# Start nginx
CMD ["/usr/local/nginx/sbin/nginx", "-g", "daemon off;"]