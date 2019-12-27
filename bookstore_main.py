import logging, configparser, mysql.connector, sys
import xml.etree.ElementTree as ET

def db_connection(hostname, username, password, port, db_name):
    '''
    Method will create MYSQL Db Connection and return connection object
    return: connection obj
    '''
    try:
        conn = mysql.connector.connect(
            host=hostname,
            user=username,
            passwd=password,
            database=db_name,
            port=port)
    except Exception as e:
        logger.error("DB Connection {}".format(e))
        sys.exit(1)
    else:
        return conn

def config_reader(filepath = None):
    '''
    Method parses config file, return dictionary of all the sections
    return: dictionary and section
    '''
    dict_option = {}
    config = configparser.ConfigParser()
    config.read(filepath)
    sections = config.sections()
    options = config.options(sections[0])
    for option in options:
        try:
            dict_option[option] = config.get(sections[0], option)
            if dict_option[option] == -1:
                logger.error("Please check Threshold Configuration File")
        except:
            dict_option[option] = None
    return sections[0] , dict_option

def xml_parser(filepath = None):
    '''
    Method parses Queries.xml file and return dictionary
    '''
    tree = ET.parse(filepath)
    root = tree.getroot()
    query_details = {}
    for child in root:
        query_details[child.attrib['id']]=child.text
    return query_details


if __name__ == '__main__':
    # Logger Configuration
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    fileHandler = logging.FileHandler(filename='app.log')  # Relative Path
    fileHandler.setFormatter(formatter)
    logger.setLevel(level=logging.DEBUG)  # Logging Level

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    #Fetch db_server and db_details from connection.ini
    db_server, db_details = config_reader(filepath = 'connection.ini') #relative path
    logger.info("Db Details {}".format(db_details))

    #Fetch queries from queries.xml file
    query_details = xml_parser('queries.xml') #relative path
    logger.debug("Query details \n{}".format(query_details))

    #Create connection object
    db_conn = db_connection(db_details['hostname'], db_details['username'],
                    db_details['password'], db_details['port'],
                    db_details['database'])

    #Create cursor object
    curr = db_conn.cursor()

    #Execute SQL queries
    #Drop Tables
    curr.execute(query_details['set_FKC_0'])
    curr.execute(query_details['drop_books'])
    curr.execute(query_details['drop_publisher'])
    curr.execute(query_details['drop_author'])
    curr.execute(query_details['drop_books_inventory'])
    curr.execute(query_details['drop_customer'])
    curr.execute(query_details['drop_orders'])
    curr.execute(query_details['drop_order_item'])
    curr.execute(query_details['set_FKC_1'])

    #Create Tables
    curr.execute(query_details['create_books'])
    curr.execute(query_details['create_publisher'])
    curr.execute(query_details['create_author'])
    curr.execute(query_details['create_books_inventory'])
    curr.execute(query_details['create_customer'])
    curr.execute(query_details['create_orders'])
    curr.execute(query_details['create_order_item'])

    #Insert Tables
    curr.execute(query_details['insert_books_1'])
    curr.execute(query_details['insert_books_2'])
    curr.execute(query_details['insert_books_3'])

    curr.execute(query_details['insert_publisher_1'])
    curr.execute(query_details['insert_publisher_2'])
    curr.execute(query_details['insert_publisher_3'])

    curr.execute(query_details['insert_author_1'])
    curr.execute(query_details['insert_author_2'])
    curr.execute(query_details['insert_author_3'])

    curr.execute(query_details['insert_books_inventory_1'])
    curr.execute(query_details['insert_books_inventory_2'])
    curr.execute(query_details['insert_books_inventory_3'])

    curr.execute(query_details['insert_customer_1'])
    curr.execute(query_details['insert_customer_2'])
    curr.execute(query_details['insert_customer_3'])

    curr.execute(query_details['insert_orders_1'])
    curr.execute(query_details['insert_orders_2'])
    curr.execute(query_details['insert_orders_3'])

    curr.execute(query_details['insert_order_item_1'])
    curr.execute(query_details['insert_order_item_2'])

    #Select Tables
    curr.execute(query_details['select_books'])
    logging.info("Recordset Books Table")
    for row in curr.fetchall():
        logging.info(row)


    curr.execute(query_details['select_publisher'])
    logging.info("Recordset Publisher Table")
    for row in curr.fetchall():
        logging.info(row)

    curr.execute(query_details['select_author'])
    logging.info("Recordset Author Table")
    for row in curr.fetchall():
        logging.info(row)

    curr.execute(query_details['select_books_inventory'])
    logging.info("Recordset Books Inventory Table")
    for row in curr.fetchall():
        logging.info(row)

    curr.execute(query_details['select_customer'])
    logging.info("Recordset Customer Table")
    for row in curr.fetchall():
        logging.info(row)

    curr.execute(query_details['select_orders'])
    logging.info("Recordset orders Table")
    for row in curr.fetchall():
        logging.info(row)

    curr.execute(query_details['select_order_item'])
    logging.info("Recordset order item Table")
    for row in curr.fetchall():
        logging.info(row)

    #Close the db connection object
    db_conn.close()