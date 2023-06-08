<div align="center">

<img src="https://freesvg.org/img/1653682897science-svgrepo-com.png" alt="logo" width="200" height="auto" />

<br />

<h1>pysoda</h1>

<p>
Python package of the SODA functions for curating and sharing datasets according to the SPARC guidelines
</p>
</div>

<br />

---

## About
SODA is a desktop software that simplifies the curation and sharing of neuromodulation, neurophysiology, and related data according to the SPARC guidelines that are aimed at making data FAIR (Findable, Accessible, Interoperable, Reusable). SODA provide intuitive user interfaces that navigate users step-by-step through the process of preparing and submiting their datasets according to the SPARC guidelines. While using the SODA app can be convenient for most investigators, others with coding proficiency may find it more convenient to implement automated workflows. To help such investigators, we are envisioning to regroup relevant functions from the Python backend of SODA into a Python package tentatively called pysoda. The backend of SODA contains many functions necessary for preparing and submitting a dataset that is compliant with the SPARC Data Structure (SDS) such as creating standard metadata files, generating manifest files, automatically complying with the file/folder naming conventions, validating against the SDS validator, uploading dataset to Pennsieve with SDS compliance (ignoring empty folders and non-allowed files, avoiding duplicate files and folders, etc.). Pysoda will make these functions that have been thoroughtly tested and validated easily integratable in automated workflows such that the investigators do not have to re-write them.
