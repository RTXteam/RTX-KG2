# Install Docker on MacOS via Homebrew

(Adapted from a blog post by Yuta Fujii, https://medium.com/@yutafujii_59175/a-complete-one-by-one-guide-to-install-docker-on-your-mac-os-using-homebrew-e818eb4cfc3). These instructions have been tested
on MacOS version 10.14.6 with Homebrew version 2.4.3. YMMV.

- Install homebrew

        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    
- Backup your Homebrew configuration (see https://tomlankhorst.nl/brew-bundle-restore-backup/)

        brew tap Homebrew/bundle
        brew bundle dump

   save the `Brewfile` someplace safe, in case you later need to restore your Homebrew system to its 
   last-known-good state.

- Install Docker:

        brew install docker docker-machine
        brew cask install virtualbox
        docker-machine create --driver virtualbox default
        docker-machine env default
        eval "$(docker-machine env default)"

   Note that the `brew cask install virtualbox` command may require you to enter
   a password, and will probably require you to go into the `System Preferences
   application` => `Security preference` panel, where you will need to click on
   `Allow` next to `Oracle`.
   
- Test your Docker installation:

        docker run hello-world
        
   which should respond with:
   
```
   Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
1. The Docker client contacted the Docker daemon.
2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
(amd64)
3. The Docker daemon created a new container from that image which runs the
executable that produces the output you are currently reading.
4. The Docker daemon streamed that output to the Docker client, which sent it
to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
$ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
https://hub.docker.com/

For more examples and ideas, visit:
https://docs.docker.com/get-started/
```

# Shut down the Docker server

    docker-machine stop default
    
# Restart the Docker server

    docker-machine start default
    eval "$(docker-machine env default)"

