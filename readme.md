# Vipunen API lukija

Vipunen on julkaissut API:n, jonka kautta saa haettua korkeakoulujen tietoja. Haettavan tietojoukon sisältöön kuuluu mm. lukumäärät vuosittain 55 op suorittaneista opiskelijoista oppilaitoksittain, yliopistojen taseet ja tuloslaskelmat, julkaisujen määrät ja ylioppilastutkintojen arvosanat lukioittain. Täysi kuvaus palvelusta on [Vipusen sivuilla](https://vipunen.fi/fi-fi/Sivut/Vipunen-API.aspx).

Tässä repossa on koodinpätkiä, joilla voi luoda itselleen AWS:ään tietokantapalvelimen instanssin käyttäen Terraformia, ja sen jälkeen Vipusen kautta saatavan datan voi hakea luodulle tietokantainstanssille Python-koodilla.

HUOM. Terraform-konfiguraatio perustaa pilveen resursseja, jotka maksavat rahaa. Käytä omalla vastuullasi.

### Tietojoukon kuvaus ja dataflow
Kaikki saatavilla olevat tietojoukot löytyvät [Vipusen sivuilta](http://api.vipunen.fi/api/resources). Esimerkiksi haettaessa Windowsin komentorivin avulla:

    $ curl http://api.vipunen.fi/api/resources/avoin_yliopisto/data?filter=tilastovuosi==2018

Tuloksena palautuu JSON-dumppina avoimessa asyliopistossa opiskelleiden määrät vuosittain ja yliopistoittain.
![Vipunen API avoin yliopisto 2018](https://s3.eu-north-1.amazonaws.com/antti-vipunen-github/vipunen_readme_kuva1.PNG "http://api.vipunen.fi/api/resources/avoin_yliopisto/data?filter=tilastovuosi==2018")

Datan siirron kuvaus on jokseenkin kuvan mukainen:
![Data dataflow'n karkea kuvaus](https://s3.eu-north-1.amazonaws.com/antti-vipunen-github/vipunen_readme_kuva3.PNG)
1. Data haetaan Python-koodilla Vipusesta.
2. Data konvertoidaan JSON:sta pandas dataframeksi, ja siirretään SQL Alchemyllä tietokantaan.
3. Data visualisoidaan visualisointiohjelmistolla, esimerkiksi Tableau Publicilla.

## Käyttö
### Esivaatimukset
* Pilveen perustettavaa tietokantapalvelinta varten tarvitaan AWS-tili ja sinne IAM-tunnus riittävillä oikeuksilla.
* Muussa tapauksessa tietokantapalvelimen ja siellä olevan tietokannan yhteysasetukset.
* Python 3 -asennus
* [Terraform.exe](https://www.terraform.io)
* Python-riippuvuudet:
    * requests
    * json
    * pandas
    * sqlalchemy

Tarvittavat paketit asentuvat pip:llä:

    $ sudo pip3 install pandas sqlalchemy

## Esimerkki konfiguraatiosta
1. Aseta main.tf-tiedostoon omat IAM-tunnuksesi tiedot sekä tietokantapalvelimen tiedot (ainakin palvelimen nimi, admin-tunnus ja sen salasana).
2. Lataa terraform.exe ja aseta sen sijainti pathiin, tai siirrä se koodikansioon. Suorita:


    $ terraform init
    $ terraform plan
    $ terraform apply

Suorituksen jälkeen ruudulle tulostuu tietokantapalvelimen yhteysasetukset.
![Vipunen API avoin yliopisto 2018](https://s3.eu-north-1.amazonaws.com/antti-vipunen-github/vipunen_readme_kuva2.PNG "terraform apply endpoint")

Todennäköisesti joudut muuttamaan instanssin turvallisuusasetuksia AWS:ssä, jotta saat yhteyden instanssiin. Lisäksi joudut luomaan palvelimelle tietokannan, jotta pääset populoimaan tauluja.

3. Tämän jälkeen voit suorittaa Python-koodin. Aseta tähän Terraformista/AWS:stä haetut tietokantainstanssin yhteysasetukset.
![api.py-parametrit](https://s3.eu-north-1.amazonaws.com/antti-vipunen-github/vipunen_readme_kuva4.PNG)
4. Suorita Python-koodi. Ohjelma hakee Vipusesta yhden tietojoukon kerrallaan, luo tietokantapalvelimelle luotuun tietokantaan taulun, ja populoi sen. Toim. huom. kaikkien tietojen siirtämisessä SQL Server Express Editionilla pyörivään kantaan kesti itsellä 5-7 päivää.
5. Tutki dataa. Tietojoukoilla on avaimet, ja kunkin taulun tiedot saa käsiteltyä joko sellaisenaan, yhdistettynä muihin tauluihin, ja visualisoitua melko järkevästi.

![Tietokantakysely](https://s3.eu-north-1.amazonaws.com/antti-vipunen-github/vipunen_readme_kuva6.PNG)

## Datan visualisointia
Esimerkki '55 op suorittaneet'-tietojoukon visualisoinnista löytyy allekirjoittaneen [Tableau Public-tililtä](https://public.tableau.com/profile/avecci#!/vizhome/Suorittanut_55op/55opsuorittaneidenmrvuosittain).
![Esimerkki visualisoinnista](https://s3.eu-north-1.amazonaws.com/antti-vipunen-github/vipunen_readme_kuva5.PNG)

## Linkkejä
- [Vipunen](https://vipunen.fi/fi-fi/Sivut/Vipunen-API.aspx)
- [Hashicorp Terraform](https://www.terraform.io)
- [Terraform RDS module](https://registry.terraform.io/modules/terraform-aws-modules/rds/aws)
- [AWS RDS](https://aws.amazon.com/rds/)
- [Tableau Public](https://public.tableau.com/profile/avecci#!/)
