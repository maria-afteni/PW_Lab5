import argparse
from urllib.parse import urlparse, quote, parse_qs
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
import json
import socket
import ssl
import re

HTTPS_PORT = 443
HTTP_PORT = 80
DB_NAME = 'cash.json'


def parse_url(url):
    parsed_url = urlparse(url)

    scheme = parsed_url.scheme
    host = parsed_url.netloc
    path = parsed_url.path

    return scheme, host, path


def send_http_get_request(host, port, path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    if port == 443:
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=host)

    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    sock.sendall(request.encode())

    response = b""
    while True:
        data = sock.recv(2048)
        if not data:
            break
        response += data

    sock.close()
    
    headers, body = response.split(b"\r\n\r\n", 1)
    headers_str = headers.decode('utf-8')
    body_str = body.decode('utf-8', 'replace')

    if re.match(r"HTTP/1.1 3\d{2}", headers_str) and 'Location: ' in headers_str:
        location = re.search(r"Location: (.+)\r\n", headers_str).group(1)
        scheme, host, path = parse_url(location)
        port = HTTPS_PORT if scheme == 'https' else HTTP_PORT
        
        return send_http_get_request(host, port, path)

    return headers_str, body_str


def parse_html_body(html_body):
    soup = BeautifulSoup(html_body, 'html.parser')
    body_text = soup.body.get_text(separator='\n\n', strip=True)

    return body_text.strip()


def parse_search_response(html_body):
    soup = BeautifulSoup(html_body, 'html.parser')
    
    final_results = []
    index = 1
    results = soup.find_all('div', class_='egMi0 kCrYT')

    while index <= len(results):
        link = results[index - 1].findChild('a')
        url = link['href']

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        valid_url = query_params.get('q', [''])[0]
        
        desc_div = results[index - 1].findChild('div', class_='BNeawe vvjwJb AP7Wnd')
        desc = desc_div.get_text()

        final_results.append(f"{index}. {desc};\nAccess link: {valid_url}\n\n")
        index += 1

    return final_results


def google_search(terms):
    query = '+'.join(quote(term) for term in terms)
    url = f"https://www.google.com/search?q={query}"
    _, host, _ = parse_url(url)
    path = f"/search?q={query}"
    port = HTTPS_PORT

    _, body = send_http_get_request(host, port, path)
    return parse_search_response(body)


def main():
    cashed_results = TinyDB(DB_NAME, indent=4)

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='Make an HTTP request to the specified URL and print the response')
    parser.add_argument('-s', nargs='+', help='Make an HTTP request to search the term using google search engine and print top 10 results')

    args = parser.parse_args()



if __name__ == "__main__":
    main()