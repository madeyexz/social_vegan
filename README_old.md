# Social Vegan

A [BackDrop Build](http://backdropbuild.com) project, made by [Ian Hsiao](https://github.com/madeyexz).

## About the Project

*Socail Vegan* is essentially a dating app for serious daters with embeddings and vector database. It's a project to explore the possibility of using OpenAI's embedding model to build match-making services.


In this version, we collect users' core value on intimate relationship (limited to 100 words, stored in the variable `expectation`), pip this into OpenAI's `text-embedding-ada-002` model, and store the vectors (or the embeddings) on Pinecone vector database and local database (`SQLite3` based). For each user's vector, we then retrieve the nearest `2` vectors from the database, which represent people with most similar expecatation, and return the corresponding `user_id`s as match results. Using the `user_id`s, we can then retrieve the user's profile from the database, display it to the user, compare it to the users and finally let them decide whether to contact the other person.

### Built With
 - Python, as the main programming language.
 - OpenAI's `text-embedding-ada-002` model, as the main embedding model.
 - Pinecone, as the vector database.
 - SQLite3, as the local database.
- 

**Limitations & Risks**

This project ultilizes the OpenAI second generation embedding model `text-embedding-ada-002`, the limitations & risks of using the model is described [here](https://platform.openai.com/docs/guides/embeddings/limitations-risks). Some key points are:
- The models encode social biases, e.g. via stereotypes or negative sentiment towards certain groups.
- Models lack knowledge of events that occurred after [Sep 2021](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings?lang=python).

**Specs**
- Semantic space dimension = `1536`.

retrieve K nearest embedding vectors

**Know Issues**
- You can't specity homosexual or heterosexual results (it's a bug).
- \[fixed\] Prone to Rate Limit Error, 

**TO-DO**
- fix the prompt