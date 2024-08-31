# Slacker: Fast Distribution with Lazy Docker Containers

## Section 2 : Docker Background
### 2.1 Version Control for Containers
- With Docker, a single command such as “docker run -it ubuntu bash” will pull Ubuntu packages from the Internet, initialize a file system with a fresh Ubuntu installation, perform the necessary cgroup setup, and return an interactive bash session in the environment
- Ubuntu is the name of an *image*
- Images are read-only copies of file-system data, and typically contain application binaries, a Linux distribution, and other packages needed by the application.
- Commands
  - Run : Performs an image
  - Pull : Fetches an image from a registry
  - Push : Uploads an image to a registry
  - Bash : The command to run in the container
- Ruby on Rails : Ruby is build on top of Rails, which is built on a debian image
- Commit : Save the state of a container as a new image
- Docker worker machines run a local docker : Docker 
### 2.2 Storage Driver Interface
- Host Directory Mounting : Docker can mount a directory from the host machine into the container
- Docker Layer Storage : Docker uses a copy-on-write storage driver to manage the file system of a container
- Get: Requests that the driver mount a layer and return a path to the mount point. This mount point should provide a view of not just the specified layer (id) but also all its ancestor layers.
- Put : Unmounts a layer
- Create : Copies data from a parent layer to create a new layer. If the parent is NULL, the new layer is empty. 
- Diff : Converts the layer from the local representation to a compressed tar file containing the files of the layer
- Applydiff : Decompresses the tar file and applies the changes to the local representation of the layer
  
### 2.3 AUFS Driver Implementation
- A commonly used docker storage driver
- This driver is built on top of the AUFS file system, which is a union file system that does not store data directly on disk but uses another file system (such as ext4) as its underlying storage.
- User Mount Point : AUFS provides a union mount point that offers a combined view of multiple directories in the underlying file system. When AUFS is mounted, it takes a list of directory paths from the underlying file system.
- Path Resolution : 