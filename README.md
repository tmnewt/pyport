# Python Finance Portfolio Research (ongoing development)

***This README is always out of date and will remain that way until the First stable release***

README last updated on: **March 20th, 2021**

**Pyport is a work in progress. Nothing here is final or guaranteed!**

PyPort was a framework aimed at helping finance nerds. This project emerged out of the developer's obsessive compulsion to automate everything and to assist him in researching an investment theory. To do this he needed a framework for systematically creating, manipulating, altering, and testing portfolio strategies on historical data. So built one from scratch...

Along the way the goal of pyport has morphed into providing tools necessary for quickly altering variable inputs used in creating portfolios, producing and saving results, and quantifying changes through a logical framework.

More info coming soon.

# Installation

## Install with pip

Package coming soon... Sorry, you'll have to follow the manual setup

## Manual setup

Requirements:
* Any python version after `3.8.8`. Earlier versions ***might*** work... (still figuring that out)

Instructions
1. Recommended you set up a new virtual environment.

1. Change directory to wherever you want to store the environment 

1. Create the environment.

1. Activate the environment.

1. Clone the `pyport` repo from github:

1. Change directory to the wherever you cloned the repo and go into the pyport directory. 
    
    * Make sure your python virtual environment is activated...

1. Install `requirements.txt`
    ```
    pip install -r requirements.txt
    ```
Everything should be ready.

If you are having trouble, please go to the discussion tab. In-depth guides will be added there sometime in the near future.

# Understanding pyport

## PyPort Storage:

More info coming soon.

## Providing input instructions:

Running a pyport requires an input file containing attribute-value pairs which map to attributes and properties of PyPort. In short, these inputs serve as ***instructions*** for pyport. A detailed guide of required and optional attribute pairs will be added in the near future. An example file which declares all possible inputs for the pyport can be found at `pyport_examples/pyports/silly.json`. Please note that some attributes-pairs are simple place holders for things in development and are not actually necessary.

pyport ***instructions*** can only be loaded through `JSON` files. This is because `JSON` uses attribute-value pairs and is easy to work with as python dictionaries. Mapping instructions from the file into python becomes pretty straightforward. The advantage of being able to quickly read inputs and then turn around and write new instructions which can then be read later was crucial to PyPorts original goal. Additionally creating new types of instructions through the attribute-value pairs means you can easily extend the framework to fit your needs. It is 100% guaranteed that more attribute-value pairs will be added in the future which makes `JSON` the ideal choice. Lastly, `JSON` makes pyports `CRUD` operations much more straightforward helping cut down on bullshit. I have no plans to support loading pyports from any other file format. However I do have plans to create a tool which will help you build out all the necessary pyport instructions through a command-line (or maybe a GUI if I'm really feeling up to it) and save the pyport instructions to allow for future reruns.

The json instructions contain 2 primary attribute-value pairs: `"universe"` and `"commands"` (There is also an additional attribute `"description"` which is for your convenance). 

## Universe

The `universe` defines the PyPort's ***universe*** which is essentially a file name of a dataset containing all the applicable data. The name is typically the same simple name as the pyport file's name (though this naming convention isn't strictly enforced). The framework then checks your computers' PyPort storage (see storage management) for the dataset. If the DataFrame is not found it will fetch all the necessary data to build the universe. By default it will then save this data under the name of the universe, saving you time in the future. More about the `universe` will be covered in the guide (coming soon).


## Commands

The `commands` are a set of ***basic*** instructions for how trading / portfolio strategies are to be run. ***Basic*** is the key word here as the commands ideally serve as fallback instructions for how things should operate without more sophisticated instructions. More info to come soon...

## A lot more stuff coming soon...


# Useful features

Info coming soon...

# Upcoming features:

Coming (sometime) soon.

* **More efficient data gathering**

    Harder better faster.

* **New data sources**
    
    Stop hitting Yahoo through pandas data reader. Soon we will have more locations to pull data from. (Remember you can always bring your own data... you don't have to use the framework to retrieve data.)

* **PyPort Parallel Universe**

    Do you find declaring pyport universe bounds limiting. Why can't we add or remove assets to the universe (or the strategy) whenever we want? PyPort could benefit from even **more** automation! I'm already on it. The pyport parallel universe feature aims to fix many of these issues and much much more. Use new tools to easily change trading/portfolio strategies on the fly. Gain more control over your strategy timelines by hooking up conditional events.  Even better it aims to create a record of actions taken to produce a paper trail which can be used to reliably rerun/recreate outcomes(like jupyter notebooks, but better...)


* **PyPort Accurate Costs**

    This update aims to fix the lack of costs. Finally, you can add in trading costs helping you to get a better idea if your strategy is profitable.

* **PyPort Assistant:**

    Can't be bothered to create and store your own pyport instructions file from scratch? Afraid you'll mess up the syntax? Or simply want to interactively explore the features of pyport? Then the pyport assistant is for you.

* **PyPort Visualization**

    Maybe...

* **PyPort High Frequency Support**

    Maybe...



# Help me
There is a ton of work which still needs to be completed. There are so many core features which are missing. This is my passion project but even I have limited time. I'd like to soon have release the first stable version in the near future. If you'd like to help out, (or want me to walk you through what exactly I'm attempting here) please leave a post over on the [discussion](https://github.com/tmnewt/pyport/discussions) tab or email me directory at timothy.newton.cma13@gmail.com and I'll get back to you ASAP.

Also, I am not a quant myself but I have considered becoming one. I'm unsure if I have the skills necessary though. I do have a Masters in Finance. I currently live near downtown Chicago. If you would like to assist in my journey (or just want to give me some tips) you can reach me