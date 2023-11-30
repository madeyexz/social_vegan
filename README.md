<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->




<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#known-issues">Known Issues</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#limitations-and-risks">Limitations and Risks</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->


*Social Vegan* is essentially a dating app for serious daters with embeddings and vector database. It's a project to explore the possibility of using OpenAI's embedding model to build match-making services.


In this version, we collect users' core value on intimate relationship (limited to 100 words, stored in the variable `expectation`), pip this into OpenAI's `text-embedding-ada-002` model, and store the vectors (or the embeddings) on Pinecone vector database and local database (`SQLite3` based). For each user's vector, we then retrieve the nearest `2` vectors from the database, which represent people with most similar expecatation, and return the corresponding `user_id`s as match results. Using the `user_id`s, we can then retrieve the user's profile from the database, display it to the user, compare it to the users and finally let them decide whether to contact the other person.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

 - Python, as the main programming language.
 - OpenAI
   - `text-embedding-ada-002` model, as the main embedding model.
   - `gpt-3.5-turbo-1106` model, to perform completion task
 - Pinecone, as the vector database.
 - SQLite3, as the local database

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.
### Prerequisites
1. get an OpenAI api key at [OpenAI](https://platform.openai.com).
2. get a Pinecone api key at [Pinecone](https://www.pinecone.io/)
3. create a Pinecone index on [Pinecone dashboard](https://app.pinecone.io), and set the index name to `socialvegan`.
4. export the API_KEYs to environment variables
    ```bash
    export OPENAI_API_KEY=<your key>
    export PINECONE_API_KEY=<your key>
    ```

### Installation
1. clone this repo to your local machine
    ```bash
    git clone https://github.com/madeyexz/social_vegan.git 
    ```
2. Install the dependencies
    ``` bash
    pip install openai, pinecone, sqlite3, tenacity
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Modify the user data (as of current, the preset data)

    In `main.py`, you will find the following code snippet:
    ```python
    # main.py
    # ...
    def main():
      # ...
      preset_data = [
            ["James",
            34,
            True,
            True,
            "US",
            "james34@example.com",
            "Jame's core value"],
            ["Sophia",
            28,
            False,
            True,
            "UK",
            "sophia28@example.co.uk",
            "Sophia's core value",]
            # and some more
      ]
    # ...
    ```
    Each person's data is stored in the `preset_data` list, and each person's data is stored in a list. The order of the data is as follows:

    `[name, age, is_male, is_heterosexual, city, email, expectation]`

    You can modified preset data
    - the number of the preset datas is *unlimited*, but keep in mind that large number of data will slow down the program, as we will encounter `RateLimitError` when we try to embed the data.

    An example of `expectation` is: 

    >*In an intimate relationship, I value honesty and communication above all. Trust is the foundation of any strong relationship, and it's something I take very seriously. I believe in being open and transparent with my partner, sharing thoughts, feelings, and experiences freely. Mutual respect is also paramount; respecting each other's individuality, space, and opinions helps in nurturing a healthy bond. I also think it's important to support each other's goals and dreams, as growing together strengthens the relationship. Lastly, a sense of humor and the ability to enjoy life's simple moments together make every day special.*

2. Modify the person you want to query at the end of the file by changing the index

    ```python
    # main.py
    # ...
    def main():
      # ...
      # get the result of person with index 0
      user_id = ids[0]
      # ...
    ```

3. Run the program
    ```bash
    python3 main.py
    ```

4. You should see results like this

    > You (Aisha) are matched with James with a score of 0.954092443!

    >Your expectation is: I believe the core of any intimate relationship is mutual respect and empathy. Understanding and caring for each other's emotional and physical well-being is paramount. I value honesty and integrity; being truthful and upfront builds trust. I also look for a sense of humor and light-heartedness in a partner, as I believe laughter and joy are essential in life. Supporting each other's ambitions and being each other's cheerleader in life's journey is something I hold in high regard.

    > James's expectation is: In an intimate relationship, I value honesty and communication above all. Trust is the foundation of any strong relationship, and it's something I take very seriously. I believe in being open and transparent with my partner, sharing thoughts, feelings, and experiences freely. Mutual respect is also paramount; respecting each other's individuality, space, and opinions helps in nurturing a healthy bond. I also think it's important to support each other's goals and dreams, as growing together strengthens the relationship. Lastly, a sense of humor and the ability to enjoy life's simple moments together make every day special., and his/her email is james34@example.com

    > It sounds like you and this person have similar expectations and values when it comes to intimate relationships. Here are five reasons why you might make a good match:

    > - Mutual respect and empathy: Both of you prioritize mutual respect and empathy in a relationship, showing that you are both considerate of each other's feelings and well-being.

    >- Honesty and transparency: You both value honesty and open communication, which creates a foundation of trust and understanding in the relationship.

    > - Support for each other's ambitions: Both of you emphasize the importance of supporting each other's goals and dreams, indicating that you are both willing to be each other's cheerleaders in life's journey.

    > - Sense of humor and enjoyment of life: You both appreciate a sense of humor and the ability to enjoy life's simple moments, suggesting that you can find joy and laughter in each other's company.

    >- Shared values in nurturing a healthy bond: Your expectations align in respecting each other's individuality, space, and opinions, indicating that you both understand the importance of nurturing a healthy and balanced relationship.


    ![screenshot_1](https://github.com/madeyexz/social_vegan/blob/main/screenshots/result_1.png)


    ![screenshot_2](https://github.com/madeyexz/social_vegan/blob/main/screenshots/result_2.png)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Known Issues -->

## Known Issues
- [ ] You can't specity homosexual or heterosexual results (it's a bug), and as of current do not support non-binary genders.
- [ ] The embedding model is prone to `Rate Limit Error`

<!-- ROADMAP -->
## Roadmap

- [ ] Create a UI, or a web interface
- [ ] Allow custom user input
- [ ] Collect user feedback
    - [ ] Tweak the GPT prompt to make it more suitable for the task
    - [ ] Try out different the user input (i.e. the `expectation` collected) to find out what's best for dating.

See the [open issues](https://github.com/madeyexz/social_vegan/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Limitations and Risks
This project ultilizes the OpenAI second generation embedding model `text-embedding-ada-002`, the limitations & risks of using the model is described [here](https://platform.openai.com/docs/guides/embeddings/limitations-risks). Some key points are:
- The models encode social biases, e.g. via stereotypes or negative sentiment towards certain groups.
- Models lack knowledge of events that occurred after [Sep 2021](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings?lang=python).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU Affero General Public License v3.0. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

- Email me: [ian.xiao@stu.pku.edu.cn](emailto:ian.xiao@stu.pku.edu.cn)

- Project Link: [Social Vegan](https://github.com/madeyexz/social_vegan)

<p align="right">(<a href="#readme-top">back to top</a>)</p>