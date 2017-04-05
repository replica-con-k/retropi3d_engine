RetroPi3D
=========
RetroPi3D en una librería de python para utilizar [Pi3D]{https://github.com/tipam/pi3d} de forma sencilla. Esta orientada a los juegos clásicos aunque utilice un motor 3D moderno.

Preparar virtualenv
===================
Se recomienda el uso de `python-virtualenv` para preparar el entorno de ejecución y desarrollo. Se incluye un archivo `requeriments.txt` para instalar todos los paquetes de forma automática, no obstante algunos de ellos no están en el repositorio de `pip` por lo que deben instalarse a parte. Una vez activado el `python-virtualenv` instalamos los requisitos::

     $ pip install hg+http://bitbucket.org/pygame/pygame
     $ pip install git+https://github.com/tito/cymunk.git
     $ pip install -r requeriments.txt

Para que los dos primeros comandos funcionen correctamete has de tener instalados Mercurial y GIT, así como diversas librerías de desarrollo. En sistemas Debian/Ubuntu esto puedes lograrlo con los siguientes comandos::

     $ sudo apt-get build-dep python-pygame
     $ sudo apt-get install mercurial git
     
