import requests
import requests
 


def get_proxy_list(show_msg = True, http_mode = "all" ):
    """
    //free-proxy-list.net API for Python 3 by Flareonz44//
    
    Returns a list of proxies in the following format:
    
    [IP Address, Port, Country Code,  Country Name, Anonymity Level, Google, HTTPS, Last Checked]
    
    if show_msg is set to False, all info messages will be supressed
    
    http_mode:
        "all" to get https and http proxies
        "http" to get only http
        "https" to get only https
    
    https://github.com/Flareonz44/free-proxy-list.net_API
    """
    if show_msg: print("[i] Setting up session...")
    req_session = requests.Session()
    req_session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'
    })
    if show_msg: print("[i] Requesting list...")
    req_response = req_session.get("https://free-proxy-list.net/")
    raw_site = req_response.text
    req_session.close()
    if show_msg: print("[i] Processing data...")
    raw_table = raw_site[
        raw_site.index("<table class=\"table table-striped table-bordered")
        :
        raw_site.index("</table>", raw_site.index("table table-striped table-bordered"))+8
    ]
    raw_table = raw_table[
        raw_table.index("<tbody>")+7
        :
        raw_table.index("</tbody>")
    ]
    rt_processed = raw_table.split("<tr>")[1::]
    for i in range(len(rt_processed)):
        raw_data = rt_processed[i]
        rd_processed = raw_data.split("</td>")[0:-1]
        for j in range(len(rd_processed)):
            rd_processed[j] = rd_processed[j][rd_processed[j].index(">")+1::]
        rt_processed[i] = rd_processed
    if show_msg: print("[i] Process complete")
    if http_mode == "http":
        http_list = []
        for each in rt_processed:
            if each[6] == "no":
                http_list.append(each)
        return http_list
    elif http_mode == "https":
        https_list = []
        for each in rt_processed:
            if each[6] == "yes":
                https_list.append(each)
        return https_list
    else:
        return rt_processed