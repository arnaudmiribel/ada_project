# Patents in Switzerland

| Soufiane El Badraoui | Arnaud Miribel | Yu Yamashita |
|:---:|:---:|:---:|:---:|

## Abstract

A patent is an exclusive right granted by a country to an inventor, allowing the inventor to exclude others from making, using or selling his or her invention in that country during the life of the patent.  
Although patents deposits are public, exploring them is hard : 
- Open APIs are rare
- Knowledges involved are sometimes very technical and prevent non-scientific people from understanding the big picture  

And yet there's little to deny that patents are true drivers for innovation, economy and competitions in today's world. In this project, we will try to give insights on patents : who deposits how many patents ? About what? Switzerland will be our use-case.

## Data description

Patents abstracts, authors, publication-dates

Our data source is the [European Patent Office](https://developers.epo.org/) database. It is a free database with over 90 million patents and it provides a REST API. From that API we can query patents and get information on the following fields :

- `patent ID`
- `country`
- `date`
- `author`
- `abstract`
- `full text`
- `bibliography`
- `claims`

See the developer portal screenshot below :

<img src="https://s13.postimg.org/5o402ok8n/Capture_d_e_cran_2016_11_06_a_21_30_30.png">

## Feasibility and Risks

- Data collection not so easy
	- Frequent sparse fields
	- Maybe not so many about Switzerland
- Data analysis difficulties
	- Many different languages (hard for NLP tasks - topic extraction). Already only in Switzerland french, italian and german... Translating is not always very good - unless Google, but their API costs.

## Deliverables

- Topic extraction (LDA) & projection (t-SNE, PCA) with potentially a `time` slider to see evolution of patents topics over time. Example below
<img src="https://lvdmaaten.github.io/tsne/examples/reuters_tsne.jpg" style="width:100%">

- Graph of relations between companies / researchers

<img src="http://www.technology.org/texorgwp/wp-content/uploads/2014/08/social_graph-600x447.jpg" style="width:400px">  


- *(Extension to international patents)* Find most publishing companies / countries / swiss companies   
<img src="https://upload.wikimedia.org/wikipedia/commons/1/17/World_population_density_map.png">

- *(if enough time)* Cross these innovation features with other data (HDI, GDP) : Does innovation correlates with human development ? with gross domestic product ?

## Timeplan

* November 31st - Data collection & data cleaning
* Mid December - Data exploration, some visualizations
* Symposium - Final visualizations ready, neat and reproducible code