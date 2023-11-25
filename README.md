# Social Vegan

A [BackDrop Build](http://backdropbuild.com) project, for more BDB projects, visit [here](https://backdropbuild.com/v2/directory).

** Limitations & Risks **

This project ultilizes the OpenAI second generation embedding model `text-embedding-ada-002`, the limitations & risks of using the model is described [here](https://platform.openai.com/docs/guides/embeddings/limitations-risks). Some key points are:
- The models encode social biases, e.g. via stereotypes or negative sentiment towards certain groups.
- Models lack knowledge of events that occurred after [Sep 2021](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings?lang=python).

** Specs **
- Semantic space dimension = `1536`.

retrieve K nearest embedding vectors

