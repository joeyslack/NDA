# Scraping for Paula.csv skincare stuff
from pathlib import Path
import time
import re
import random
import sys

# import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import psycopg2
from config import load_config

options = uc.ChromeOptions()
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument(
    f"--load-extension={Path(__file__).parent}/extensions/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_57_0_0/"
)

driver = uc.Chrome(headless=False, use_subprocess=True, options=options)


# Database setup
def connect(config):
    """Connect to the PostgreSQL database server"""
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print("Connected to the PostgreSQL server.")
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == "__main__":
    config = load_config(filename="ewg.ini")
    # connect(config)


def clean(item):
    return item.replace("• ", "")


# Connect to db
conn = connect(config)
curr = conn.cursor()

# USAGE:  `python ingredients.py "HIGH HAZARD" 100 0` {score} {limit} {offset}

score = sys.argv[1] if len(sys.argv) > 1 else "HIGH HAZARD"
limit = sys.argv[2] if len(sys.argv) > 2 else 100
offset = sys.argv[3] if len(sys.argv) > 3 else 0

print("Adding ingredients with SCORE LIMIT OFFSET: ", score, limit, offset)
# 1. Load items from database
curr.execute(
    "SELECT * FROM products WHERE score = %s LIMIT %s OFFSET %s", [score, limit, offset]
)
rows = curr.fetchall()
insertValues = []

for row in rows:
    href = row[5]
    try:
        driver.get(href)
    except Exception as e:
        print("Error", e)

    time.sleep(1)
    table = driver.find_element(
        By.XPATH, "//table[contains(@class, 'table-ingredient-concerns')]"
    )
    ingredients = table.find_elements(
        By.XPATH, ".//tr[contains(@class, 'ingredient-overview-tr')]"
    )
    ingredients_info = table.find_elements(
        By.XPATH, ".//tr[contains(@class, 'ingredient-more-info-wrapper')]"
    )

    for index, i in enumerate(ingredients):
        name = i.find_element(
            By.XPATH,
            ".//td[contains(@class, 'td-ingredient')]/div[contains(@class, 'td-ingredient-interior')]",
        ).text.strip()
        findnames = re.search(r"(.+)\s*Appeared as\: (.+)", name)
        if findnames is not None and findnames.group(1) is not None:
            name = findnames.group(1)

        score = i.find_element(
            By.XPATH,
            ".//td[contains(@class, 'td-score')]/img[contains(@class, 'ingredient-score')]",
        ).get_attribute("alt")[-2:]

        data_availability = ""
        try:
            data_availability = i.find_elements(
                By.XPATH,
                ".//td[contains(@class, 'td-ingredient')]/div[contains(@class, 'td-availability-interior')]/span",
            )[-1].text.strip()
        except Exception as e:
            print(e, i.get_attribute("innerHTML"))

        names = []
        try:
            # findnames = i.find_element(
            #     By.XPATH,
            #     ".//td[contains(@class, 'td-ingredient')]/div[contains(@class, 'td-ingredient-interior')]/span[contains(@class, 'orig_text')]",
            # ).text
            # print('find names:: ', findnames)
            # x = re.search(r"^Appeared as\: (.+)", findnames)
            x = findnames.group(2)
            if x is not None and x.group is not None:
                names = list(map(str.strip, x.group(1).split("/")))
        except:
            pass

        info = ingredients_info[index].find_elements(
            By.XPATH, ".//div[contains(@class, 'ingredient-more-info')]//table//tr"
        )
        functions = []
        concerns = []
        ingredient_href = ""

        if len(info) > 2:
            functions = (
                info[0]
                .find_elements(By.XPATH, ".//td")[1]
                .get_attribute("innerHTML")
                .strip()
                .split(",")
            )
            concerns = list(
                map(
                    clean,
                    info[1]
                    .find_elements(By.XPATH, ".//td")[1]
                    .get_attribute("innerHTML")
                    .split("<br>"),
                )
            )
            ingredient_href = (
                info[2].find_element(By.XPATH, ".//td/a").get_attribute("href")
            )
        elif len(info) == 2:
            functions = (
                info[0]
                .find_elements(By.XPATH, ".//td")[1]
                .get_attribute("innerHTML")
                .strip()
                .split(",")
            )
            ingredient_href = (
                info[1].find_element(By.XPATH, ".//td/a").get_attribute("href")
            )
        elif len(info) == 1:
            ingredient_href = (
                info[0].find_element(By.XPATH, ".//td/a").get_attribute("href")
            )

        try:
            id = re.search("\/ingredients\/([0-9]+)", ingredient_href).group(1)
        except:
            print(
                "No ingredient ID found: ",
                re.search("\/ingredients\/([0-9]+)", ingredient_href),
            )
            break

        product_id = [row[0]]

        insertValues.append(
            [
                id,
                name,
                names,
                functions,
                concerns,
                data_availability,
                ingredient_href,
                score,
                product_id,
                name,
                names,
                functions,
                concerns,
                data_availability,
                ingredient_href,
                score,
                row[0],
            ]
        )

if len(insertValues) > 0:
    curr.executemany(
        "INSERT INTO ingredients(id, name, names, functions, concerns, data_availability, ingredient_href, score, product_id) \
		VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) \
		ON CONFLICT (id) DO UPDATE SET (name, names, functions, concerns, data_availability, ingredient_href, score, product_id) = (%s, %s, %s, %s, %s, %s, %s, ingredients.product_id || %s)",
        insertValues,
    )
    conn.commit()

print("FINISHED. Inserted: ", len(insertValues))
conn.close()
