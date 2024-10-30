# python-samples
Sample Python coding with a lot of security and technical features, all in one rep for easy adoption.

## Programs alphabetically

* argparse-samples.py shows how to specify command line arguments into this program.
* calculator-tk.py is a calculator created using the Tk GUI library.
* dijkstras.py to compare calculations of shortest path on a graph
* dijkstra-yt.py to calculate shortest path using heapq library
* endecode-protobuf.py encodes/decodes a comma-separated list so each word in front of a # prefix has a char count, like Protobuf does for gRPC.
* num2words.py simply converts a number input to its word.
* openweather.py to obtain from API calls and format weather data as fuzzy tokens
* pengram2nato.py to use the NATO phonetic alphabet spell out a sentence.
* plotting.py to create common visualizations using matplotlib.
* python-samples.py is a conglomeration of many features.
* ml-metrics.py to use PyTorch & Scikit to generate metrics for Machine Learning.
* pytorch-mnist.py Use PyTorch to build, train and evaluate a neural network to recognize a hand written digit MNIST
* recursive-cache.py shows faster Fibonnici recursion calls when using functools cache.
* roku-set.py opens Roku at a given IP address to the YouTube video specified.
* roman2int.py converts Roman numerals to base 10 numbers.
* rot13.py is used on UseNet to encode sentences using a cypher that's 13 characters away.
* sklearn-sample calculates
* try-accept.py to show usage of try/except/else/finally exceptions
* variables.py to experiment with defining and viewing objects of various data types.
* youtube-download.py downloads videos based on its URL.

NOTE: Other pograms are in the https://github.com/bomonike organization:
* https://github.com/bomonike/memon calculate super strong word phrases and remember them via LLM gen'd songs. See https://www.youtube.com/watch?v=KAjkicwrD4I
on how to memorize using PAO (Person Action Object)

The STATUS of each program is noted within each file.

Before running each:
```
chmod +x dijkstras.py
./dijkstras.py
```


## etc.

https://codehs.com/tutorial/david/sample-a-csp-performance-task-1
Sample A CSP Performance Task

https://codehs.com/tutorial/david/sample-b-csp-performance-task
Sample B CSP Performance Task - Caesar Cipher

https://www.youtube.com/watch?v=LXsdt6RMNfY
Use Python to automate my life

https://www.youtube.com/watch?v=mCk4Rabkmjc
Automate Boring Office Tasks with ChatGPT and Python

https://www.youtube.com/watch?v=Ge-9AhVVOFc
Automate any task using ChatGPT! (my full GPT building framework)


# Run a Bash script
import subprocess
result = subprocess.run(["bash", "path/to/script.sh"], capture_output=True, text=True)
stdout = result.stdout
stderr = result.stderr


https://github.com/Gatsby-Lee/DevOps/tree/master/programming_lang/python

https://www.youtube.com/watch?v=kGcUtckifXc
Please Master These 10 Python Functions…

Have a single import per line to reduce merge conflicts.
See https://github.com/asottile/reorder-python-imports?tab=readme-ov-file#why-this-style