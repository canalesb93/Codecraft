# ![Codecraft](https://raw.githubusercontent.com/canalesb93/Codecraft/master/documents/codecraft.png)

Codecraft is a Python based programming language.
You can view a live demo at: [http://codecraft.canalesb.com/](http://codecraft.canalesb.com/)

# Requirements

Codecraft requires mainly Python, but also PHP if you want to run the web interface.
### Python v2.7.13To download python head to https://www.python.org/downloads/ and select the version 2.7.13.### PHPTo download PHP head to http://php.net/downloads.php and download a 7.1 version or higher. PHP is needed for the web interface.
# Installation and Setup
### Download
The first thing you need to do is head to our github page and download Codecraftfiles. You can find them at https://github.com/canalesb93/Codecraft.
Press the “Clone or download” button and run the link in your terminal at the desired installation directory.
```{r, engine='bash', install}$ git clone git@github.com:canalesb93/Codecraft.git```
### Project Directory
After the files have been installed, move into the codecraft directories.
```{r, engine='bash', project}$ cd Codecraft/```

The Codecraft project has three main directories:
* *interface/* - Holds the web application with the graphical input.* *compiler/* - Holds the compiler files* *samples/­* - Holds example programs
### Usage

There are 2 main ways to run the program, through the web interface or directly through your terminal.
#### Running Web Interface
To fully run the web interface you must navigate to the interfaces/ directory and run locally run a file hosting server. We recommend you use PHP for this since it allows platform code execution.
```{r, engine='bash', server}$ cd interfaces/$ php ‐S localhost:8000```

This will run the PHP built­in server feature. You can now open your browser and open [http://localhost:8000](http://localhost:8000).
Once in the site you can use blockly or the custom text editor provided to run programs.
#### Running with terminal
There are two ways to execute a program through the terminal.
###### Bash Script
To run the full execution script you must first give the file permissions. Go to the main project’s directory. And run:```{r, engine='bash', project}$ chmod +x craft```
After that you can run your program with:
```{r, engine='bash', project}$ ./craft path/to/program.craft```

###### Python Execution
You can also run the compiler by phase. First the compilation phase which generates the “.crafted” file. And then the execution phase which runs the generated file.

From the main project directory run this to compile:

```{r, engine='bash', project}$ python compiler/parser.py path/to/program.craft```
This will generate the “.crafted” file and show some information about the compilation. You must then finally give to the file to the execution script.
```{r, engine='bash', project}$ python compiler/virtual_machine.py path/to/program.crafted```