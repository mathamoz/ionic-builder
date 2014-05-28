# ionic-builder
#
# VERSION               0.0.1

FROM      ubuntu
MAINTAINER Joel Weirauch <jbw@tweakbox.net>

# make sure the package repository is up to date
RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list
RUN apt-get update

# We need fakeroot to install JDK b/c it requires access to prohibited functions
RUN apt-get install -y fakeroot
RUN fakeroot apt-get install -y default-jre default-jdk
RUN apt-get install -y git-core curl nodejs npm lib32z1 lib32ncurses5 lib32bz2-1.0 lib32stdc++6 ant unzip

# We need to be able to execute node
RUN ln -s /usr/bin/nodejs /usr/bin/node

# Install cordova and ionic
RUN npm install -g cordova ionic

# Make a directory to store the Android SDK in
RUN mkdir /Development

# Fetch and unpack the Android SDK
ADD http://dl.google.com/android/adt/22.6.2/adt-bundle-linux-x86_64-20140321.zip adt-bundle-linux.zip
RUN unzip adt-bundle-linux.zip
RUN mv adt-bundle-linux-x86_64-20140321 /Development/adt-bundle-linux
RUN rm -rf adt-bundle-linux.zip

# Fetch resty (used for reporting status back to the builder ui)
RUN curl -L http://github.com/micha/resty/raw/master/resty > resty

# Fetch our build script
RUN curl -L http://github.com/mathamoz/ionic-build/raw/master/build.sh > build.sh
RUN chmod +x build.sh
