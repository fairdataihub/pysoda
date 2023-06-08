<div align="center">

<img src="https://freesvg.org/img/1653682897science-svgrepo-com.png" alt="logo" width="200" height="auto" />

<br />

<h1>pysoda</h1>

<p>
Python package of the SODA functions for curating and sharing datasets according to the SPARC guidelines

*Note: Not currently under development. May be developed if there is need expressed.*
</p>
</div>

<br />

---

## About
[SODA](https://github.com/fairdataihub/SODA-for-SPARC) is a desktop software that simplifies the curation and sharing of neuromodulation, neurophysiology, and related data according to the [SPARC guidelines](https://docs.sparc.science/docs/data-submission-walkthrough) that are aimed at making data FAIR (Findable, Accessible, Interoperable, Reusable). While using the SODA app can be convenient for most investigators, others with coding proficiency may find it more convenient to implement automated workflows. To help such investigators, we are envisioning to regroup relevant functions from the Python backend of SODA into a Python package tentatively called pysoda. The backend of SODA contains many functions necessary for preparing and submitting a dataset that is compliant with the [SPARC Data Structure (SDS)](https://doi.org/10.1101/2021.02.10.430563) such as:
- Creating standard metadata files
- Generating manifest files
- Automatically complying with the file/folder naming conventions
- Validating against the offical SDS validator
- Uploading dataset to Pennsieve with SDS compliance (ignoring empty folders and non-allowed files, avoiding duplicate files and folders, etc.)
- And many more

Pysoda will make these functions, which have been thoroughtly tested and validated, easily integratable in automated workflows such that the investigators do not have to re-write them. This will be very similar to the [pyfairdatatools](https://github.com/AI-READI/pyfairdatatools) Python package we are developing for our [AI-READI project](https://aireadi.org/) as part of the NIH Bridge2AI program.

## Interested?
Pysoda will be developed if there is need expressed by SPARC investigators or other investigators desiring to submit their datasets for publication on the SPARC Portal. If you think pysoda could be useful to you, please let us know through the [GitHub issues](https://github.com/fairdataihub/pysoda/issues) of this repository of via email (bpatel@fairdataihub.org).
