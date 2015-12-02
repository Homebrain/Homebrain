Core
====

In the core package lies core functionality and therefore happens to contain code 
that is used across the application. Knowledge of these classes and how they work is 
required in order to be able to understand the architecture.

.. automodule:: homebrain.core
    :members:

The Agent class
---------------

The Agent class is the basis for all computing "nodes" in the architecture. 
Agents communicate to each other with messages (known as Events) via the Dispatcher.

.. autoclass:: homebrain.Agent
    :members:


The Event class
---------------

.. autoclass:: homebrain.Event
    :members:

The Dispatcher class
--------------------

.. autoclass:: homebrain.Dispatcher
    :members:

The AgentManager class
----------------------

.. autoclass:: homebrain.AgentManager
    :members:

The moduleloader module
-----------------------

.. automodule:: homebrain.moduleloader
    :members:
