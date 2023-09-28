import pandas as pd
import zeep
import zeep.helpers
import sqlalchemy
import os

WSDL = ("http://webservices.oorsprong.org/"
        "websamples.countryinfo/CountryInfoService.wso?WSDL")

MYSQL_HOST = 'db'
MYSQL_PORT = '3306'
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PW = os.environ['MYSQL_PASSWORD']
MYSQL_DB = os.environ['MYSQL_DATABASE']


def initialize_soap_client():
    return zeep.Client(
        wsdl=WSDL,
        service_name="CountryInfoService",
        port_name="CountryInfoServiceSoap"
    )


def get_country_names_and_iso_codes_from_soap_client_as_dataframe(soap_client):
    result = soap_client.service.ListOfCountryNamesByCode()
    result_as_base_python_objs = zeep.helpers.serialize_object(result)
    return pd.DataFrame(result_as_base_python_objs)


def clean_column_names(df):
    return df.rename(columns={'sISOCode': 'iso_code', 'sName': 'country'})


def convert_zeep_objects_to_dataframe(zeep_obj):
    return pd.DataFrame(zeep.helpers.serialize_object(zeep_obj))


def initialize_db_engine():
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://" + MYSQL_USER + ":" + MYSQL_PW + "@" + MYSQL_HOST +
        ":" + MYSQL_PORT + "/" + MYSQL_DB
    )
    return engine


def print_db_table_contents(engine):
    with engine.connect() as conn:
        result = conn.execute(
            sqlalchemy.text("select iso_code, country from iso_codes")
        )
        print("ISO  Country")
        print("---  -------")
        for iso_code, country in result:
            print(iso_code, " ", country)


if __name__ == "__main__":
    # extract the data from the SOAP service
    client = initialize_soap_client()
    df = get_country_names_and_iso_codes_from_soap_client_as_dataframe(client)

    # transform the data
    df = clean_column_names(df)

    # load the data into the database
    engine = initialize_db_engine()
    df.to_sql(name="iso_codes", con=engine)

    # verify the upload by printing the table to stdout
    print_db_table_contents(engine)
