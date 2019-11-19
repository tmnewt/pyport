# Python Finance Portfolio Research

Repo intended to assist backtesting portfolio strategies within python.

Most of the repo will be in the form of Jupyter notebooks detailing design, uses of code, examples of results, etc. Will also allow for others to replicate and verify others findings.

You can read the Jupyter notebooks here on Github. I will be uploading the actual code as `.py` files. If you do not see runnable code for a notebook let me know and I'll add it. I don't want anyone wasting their time copying the code from the notebooks when there should be a `.py` file. 


## The Big Picture: to eventually build a robust framework to run complex portfolio strategies.

## Summary Goal Stages:

1) ~~Writing up the original project with discussion.~~ Done!
2) Improve the code structure (pretty much rewrite all the code)
3) Overhaul new code with userful features to increas usability.
4) Overhaul the backend and work on efficiencies
5) Add paint and bells and whistles and finalize on usability
6) Major release?

Do this all while pushing out notebooks showcasing a variety of equity portfolio strategies and how they are implemented using whatever code I'm working with.

### More detailed discussion on stages.

#### Improving the code and increasing usability
The big thing here is to move away from function only scripts and rely more on classes and methods. While this ought to have been done from the beginning it's never to late to make this vital switch.

### Some vital features needed.
* ability to pull data from a variety of sources (and handle importing as well)
* ability to change observation frequency
* ability to change re-balancing frequency
* ability to test what if at any point in time
* ability to manually imput (or better yet, import) tickers and portfolio weights of a given portfolio.
* ability to record results to files (including appropriate dataframe, variables, meta data, etc)

### Some vital backend stuff needed:
* Better handling of pandas datareader (especially Yahoo data reader)
* Well defined and consistent datetime handling (including ability to smartly recognize different date formats and react accordingly).
* Performance tracking
* Speeding up optimization method
* Simple file structure for code.

##### Why I'm doing this.
I'm mainly doing this for myself so that I might learn and grow. When I worked on the original project back in graduate school I found this to be the type of work that put all my skills to use and then some. It felt like all my classes had led to this one project. By expanding this project I can keep those skills sharp and hopefully learn along the way. All feedback and/or help is appreciated!
