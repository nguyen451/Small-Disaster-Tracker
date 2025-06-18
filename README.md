# SMALL DISASTER TRACKER
#### Video Demo:  <URL HERE>
#### Description:
1. **Ideas**:
- This is a small disaster tracker, which keep track of disaster in Vietnam and show some general statistic information of it. This application give user a total look of disasters in Vietnam (such as common disasters and their frequency) and also in provinces in Vietnam.
- The data for this project is from Vietnam disaster monitor website: [thientaivietnam](http://vndms.dmc.gov.vn/). But because of the data limitation, the data in this project is just a sample or demo.
- In this project, user can refresh to get the lastest data from the web.
- There are 2 choice for user:
  - Show disaster statistics in Vietnam.
  - Show disaster statistics in one province provided by user.
2. **This project contains**:
- `project.py` : contains main functions of the project
  - `get_data` : get json data from Vietnamese disaster website: [thientaivietnam](http://vndms.dmc.gov.vn/), save raw data to `disaster_2.csv`, clean and transform data then save to `proper_data.csv` and database `vieDisasters.db`
  - `field_edit` : a function for clean and transform process, extract *province* from raw data and set as a new field in data
  - `remove_accents`, `normalize_text`: function to remove accents from original province name and turn into proper format
  - `extract_province2` : extract *province* from *kv_anhhuong* (affected area)
  - `dst_by_type` : return list of disasters and its count of occurances in one province/ in Vietnam
  - `most_freq_dst` : return the most frequence disasters in one province/ in Vietnam
  - `dst_by_prov` : count of disasters in each province in Vietnam
  - `disaster_trends` : draw plots of 5 most frequence disaster in Vietnam/ one province
- `helper.py` : additional helping functions: `get_js` (create url, get json data), `to_csv_js` (save to csv file), `make_and_print_table` (print table to terminal)
- `test_project.py` : unit test for functions in `project.py`:
  - normalize_text, extract_province2, dst_by_type, most_freq_dst, dst_by_prov



