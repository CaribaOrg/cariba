<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/CaribaOrg/cariba">
    <img src="app/static/images/caribaSmall.png" alt="Logo" height="80">
  </a>

<h3 align="center">Cariba</h3>

  <p align="center">
    Automobile Car Parts Store
    <br />
    <a href="https://github.com/CaribaOrg/cariba"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://www.fuzzfoo.tech/">View Demo</a>
    ·
    <a href="https://github.com/CaribaOrg/cariba/issues">Report Bug</a>
    ·
    <a href="https://github.com/CaribaOrg/cariba/issues">Request Feature</a>
  </p>
</div>



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
        <li><a href="#installation">Clone the repo</a></li>
        <li><a href="#installation">Create a Virtual Environment</a></li>
        <li><a href="#installation">Install Python Dependencies</a></li>
        <li><a href="#installation">Configure Environment Variables</a></li>
        <li><a href="#installation">Install Python Dependencies</a></li>
        <li><a href="#installation">Configure MYSQL</a></li>
        <li><a href="#installation">Run the Flask Application</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


Welcome to the Cariba project repository! This repository contains the source code and assets for the Cariba project that specializes in automobile parts.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Flask](https://img.shields.io/badge/flask-black?style=for-the-badge&logo=flask)](https://github.com/CaribaOrg/cariba)
[![Tailwind CSS](https://img.shields.io/badge/tailwindcss-black?style=for-the-badge&logo=tailwindcss)](https://github.com/CaribaOrg/cariba)
[![HTML](https://img.shields.io/badge/html-black?style=for-the-badge&logo=html5)](https://github.com/CaribaOrg/cariba)
[![Flask](https://img.shields.io/badge/flask-black?style=for-the-badge&logo=flask)](https://github.com/CaribaOrg/cariba)
[![Javascript](https://img.shields.io/badge/javascript-black?style=for-the-badge&logo=javascript)](https://github.com/CaribaOrg/cariba)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Follow these steps to set up the project on your local machine.
To get a local copy up and running follow these simple example steps.

### Prerequisites

- [Python3](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)

### Clone the repo:
```bash
git clone https://github.com/CaribaOrg/cariba.git
cd cariba
```

### Create a Virtual Environment
```bash
python3 -m venv my_env
```

Activate the virtual environment:
* On Windows:
```bash
my_env\Scripts\activate
```
* On Unix or MacOS:
```bash
source my_env/bin/activate
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
```bash
source misc/env_setup.sh
```

### Configure MYSQL
```bash
cat misc/setup_mysql_dev.sql | sudo mysql
```

### Run the Flask Application
```bash
python3 --app app/run.py run
```
Visit http://localhost:5000 in your browser to see the application running.

Or visit https://www.fuzzfoo.tech for the deployed version

<p align="right">(<a href="#readme-top">back to top</a>)</p>



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

Distributed under the GPLv3 License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

- Hasbi Sabah - [linkedin](https://www.linkedin.com/in/sabahhasbi/) - sabahhasbi13@gmail.com

- Nyangasi Mhozya - [linkedin](https://www.linkedin.com/in/nyangasi-m-54467816b/) - nyangasi.m@gmail.com

- EL FADILI Abdessamad - [linkedin](www.linkedin.com/in/abdessamad-el-fadili) - elfadili.ae@gmail.com


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

We are deeply grateful to [ALX](https://www.alxafrica.com/blog/software-engineering-hard-vs-soft-skills/) team for providing us with the incredible opportunity to embark on this learning journey. Their guidance, support, and expertise have been instrumental in shaping our growth as aspiring software engineers.

## ALX and Mentors

- **ALX** - Thank you for creating an environment that fosters learning, collaboration, and personal development. ALX has been the catalyst for our journey towards becoming skilled software engineers.

- **Mentors** - A heartfelt thank you to our mentors who have generously shared their knowledge and experiences. Your guidance has been invaluable in navigating the complexities of software development, and we are truly appreciative of your commitment to our success.

## Community and Peers

We are thrilled to be part of a vibrant community where individuals come together to learn, share, and support each other. Our peers have played a significant role in creating a collaborative atmosphere that encourages growth and camaraderie.

- ** Cohort 13 Members** - To our fellow cohort members, thank you for the countless hours of collaboration, PLDs, problem-solving, and shared learning experiences. Together, we are creating a supportive community that propels us towards our common goal of becoming proficient software engineers.

---

Our journey would not be the same without the support, encouragement, and knowledge shared within the ALX community. We look forward to continued collaboration and growth together.

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/CaribaOrg/cariba.svg?style=for-the-badge
[contributors-url]: https://github.com/CaribaOrg/cariba/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/CaribaOrg/cariba.svg?style=for-the-badge
[forks-url]: https://github.com/CaribaOrg/cariba/network/members
[stars-shield]: https://img.shields.io/github/stars/CaribaOrg/cariba.svg?style=for-the-badge
[stars-url]: https://github.com/CaribaOrg/cariba/stargazers
[issues-shield]: https://img.shields.io/github/issues/CaribaOrg/cariba.svg?style=for-the-badge
[issues-url]: https://github.com/CaribaOrg/cariba/issues
[license-shield]: https://img.shields.io/github/license/CaribaOrg/cariba.svg?style=for-the-badge
[license-url]: https://github.com/CaribaOrg/cariba/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
