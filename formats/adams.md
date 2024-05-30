# ADAMS

[ADAMS](https://adams.cms.waikato.ac.nz/) reports are just [Java .properties](https://en.wikipedia.org/wiki/.properties)
files used for storing meta-data. Since these files do not store any type information, 
ADAMS reports store with each key-value pair of data an additional key-value pair that
contains the type information. As data types, the following are supported:

* `B`: boolean
* `N`: numeric (float or integer)
* `S`: string
* `U`: unknown (treated as string)

The data type appends `<TAB>DataType` to the key of the data pair. Here is an example:

```properties
# comments get ignored
A=some_kind_of_string
A\tDataType=S
B=20.0
B\tDataType=N
C=true
C\tDataType=B
```

In case of **audio classification**, a single field in the report will hold the class label.

For the **speech** domain, a single field in the report will hold the transcript.
