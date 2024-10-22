FROM nginx:mainline

# Remove the default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy your custom nginx.conf into the nginx configuration directory
COPY default.conf /etc/nginx/conf.d/
