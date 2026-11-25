<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&amp;color=0:101c2d,100:254963&amp;height=190&amp;section=header&amp;text=Open%20Research&amp;fontColor=ffffff&amp;fontSize=55&amp;fontAlignY=40&amp;desc=An%20independent%20initiative%20for%20open%2C%20collaborative%20and%20AI-assisted%20research.&amp;descAlignY=69&amp;descSize=15" width="100%" alt="Open Research. An independent initiative for open, collaborative and AI-assisted research.">

[![Contributions](https://img.shields.io/badge/contributions-open-376c59?style=flat-square)](CONTRIBUTING.md)
[![Software](https://img.shields.io/badge/software-MIT-405c78?style=flat-square)](LICENSES/MIT.txt)
[![Research](https://img.shields.io/badge/research-CC%20BY%204.0-405c78?style=flat-square)](LICENSE.md)

[Research](#research) · [Contributing](#contributing) · [Research standards](#research-standards) · [About](#about)

</div>

## Why Open Research?

For someone outside academia, pursuing a research question can be difficult. Access to equipment, computing resources, specialist knowledge and experienced collaborators is often limited. An interesting idea may go unexplored because the person who had it simply cannot investigate it.

AI is changing part of that equation. Individuals can now attempt problems that would previously have been difficult to approach without considerable resources or years of specialist training. This does not remove the need for expertise or careful verification, but it opens up new opportunities for independent research.

Open Research brings the model of open-source collaboration to research. This repository is a place to propose questions, share findings and work on problems with others. A researcher can publish a derivation here; someone else can examine it, identify a gap, develop an alternative proof or take the result further. The work, its history and the contributions of everyone involved remain accessible.

Anyone is welcome to contribute, regardless of their academic background or profession. **We judge contributions by the quality of the work.**

## Research

### Founding collection · 2026

The first collection draws on independent research by [Rudra Tiwari](https://github.com/Rtx09x), the founder of Open Research.

It covers problems in quantum error correction, physical computing, electrical network diagnosis, information theory, numerical linear algebra and the analysis of algorithms. The collection is currently being prepared for release. Each project will document its findings, supporting evidence and outstanding questions, alongside a manuscript or technical report where appropriate.

The individual projects will be linked here as they become available.

### Research domains

| Domain | Areas of interest |
| :--- | :--- |
| [Mathematics](mathematics/) | Pure and applied mathematics, information theory, numerical analysis |
| [Physics](physics/) | Theoretical physics, quantum information |
| [Applied Physics](applied-physics/) | Physical computing, interacting systems, programmable materials |
| [Computer Science](computer-science/) | Algorithms, machine learning, theory of computation |
| [Engineering](engineering/) | Electrical, mechanical and systems engineering |

These directories are a starting point. Research need not fit neatly into a single discipline, and contributors can propose additional domains.

## Contributing

You do not need a finished paper to participate. You might have a question worth investigating, an existing body of work to share, or a new approach to a problem someone else is working on.

There are several ways to get involved:

- [Propose a problem](https://github.com/Rtx09x/Open-Research/issues/new/choose), whether or not you have a solution.
- Submit original research or extend an existing project through a pull request.
- Reproduce a result, examine a proof or report an error using the [research feedback form](https://github.com/Rtx09x/Open-Research/issues/new/choose).
- Collaborate with other researchers on methods, experiments and manuscripts.

Each project has a primary research domain and its own folder. The only required structure is:

```text
domain/
└── research-project/
    ├── README.md
    ├── AUTHORS.md
    ├── archive/
    └── code/
```

Project maintainers decide how to organise everything else. The [project template](templates/project/) and [contribution guidelines](CONTRIBUTING.md) explain the requirements for submitting and maintaining research.

## Research standards

We accept work in progress, negative results and conjectures, as well as completed investigations. A submission should explain what has actually been established, how it was checked and what remains uncertain. A conjecture is welcome as a conjecture; a claimed theorem needs a proof.

AI-assisted research is encouraged. Contributors must disclose how AI was used and describe the checks performed on its output. Responsibility for the submitted work remains with its authors.

### Verification

Research can be admitted before independent review, but admission does not establish correctness. Every project records its verification status, and individual claims may have separate statuses where necessary.

| Status | Meaning |
| :--- | :--- |
| Unverified | Substantive validation has not yet been established. |
| Internally verified | The research team has documented its own checks. |
| Under independent review | An independent examination is in progress. |
| Independently verified | Independent checks support the specified result. |
| Peer reviewed | The specified result has undergone formal peer review. |
| Disputed | A material objection remains unresolved. |

See [VERIFICATION.md](VERIFICATION.md) for the full framework. Reviewers are encouraged to document the scope and outcome of their checks, including unsuccessful attempts at reproduction.

### Authorship and credit

Contributors retain copyright in their original work, subject to the permissions granted under the applicable open licence. Research built on previous work must cite its sources. Joint work should credit everyone who contributed substantively, with authorship reflecting their actual contributions.

When publishing work developed through Open Research, please acknowledge the initiative where appropriate. Cite individual research projects and their authors rather than treating the repository as a substitute for scholarly citation.

## About

Open Research was founded in 2026 by **[Rudra Tiwari](https://github.com/Rtx09x)**, an undergraduate researcher working on problems in mathematics, physics and computational science using AI-assisted methods.

The initiative grew out of his own experience investigating scientific questions independently. The founding collection is the first step towards opening that process to other researchers and building a shared body of work.

The repository is currently maintained by its founder. As more researchers participate, project maintainers and independent reviewers will take on greater responsibilities. The initiative is presently independent.

## Repository documentation

[Contribution guidelines](CONTRIBUTING.md) · [Verification standards](VERIFICATION.md) · [Governance](GOVERNANCE.md) · [Code of conduct](CODE_OF_CONDUCT.md) · [Project template](templates/project/)

Original software is available under the [MIT License](LICENSES/MIT.txt); original research material is covered by [CC BY 4.0](LICENSE.md), subject to the repository licensing policy and any identified third-party rights. Repository-level citation information is available in [CITATION.cff](CITATION.cff).

