import os

import bs4 as bs4
import requests

file_list_from_dir = '''
30.06.2021  12:41            81 667 accordion.min.js
30.06.2021  12:42            52 705 accordiontab.min.js
30.06.2021  12:42           114 345 api.min.js
30.06.2021  12:42           174 685 autocomplete.min.js
30.06.2021  12:42            64 807 avatar.min.js
30.06.2021  12:43            55 506 avatargroup.min.js
30.06.2021  12:43            56 712 badge.min.js
30.06.2021  12:44            55 676 badgedirective.min.js
30.06.2021  12:44            66 104 blockui.min.js
30.06.2021  12:44            73 454 breadcrumb.min.js
30.06.2021  12:44            70 528 button.min.js
30.06.2021  12:44           479 024 calendar.min.js
30.06.2021  12:45            58 936 card.min.js
30.06.2021  12:45           112 342 carousel.min.js
30.06.2021  12:45           170 740 cascadeselect.min.js
30.06.2021  12:46            62 707 chart.min.js
30.06.2021  12:46            66 989 checkbox.min.js
30.06.2021  12:46            70 162 chip.min.js
30.06.2021  12:46            89 531 chips.min.js
30.06.2021  12:47           156 805 colorpicker.min.js
30.06.2021  12:47            69 360 column.min.js
30.06.2021  12:47            52 484 columngroup.min.js
30.06.2021  12:47            66 792 config.min.js
30.06.2021  12:48            51 673 confirmationeventbus.min.js
30.06.2021  12:48            53 860 confirmationservice.min.js
30.06.2021  13:26            70 781 confirmdialog.min.js
30.06.2021  13:26           106 378 confirmpopup.min.js
30.06.2021  12:48           128 585 contextmenu.min.js
30.06.2021  12:49           924 424 datatable.min.js
30.06.2021  12:49            90 894 dataview.min.js
30.06.2021  12:50            57 582 dataviewlayoutoptions.min.js
30.06.2021  12:50            58 423 deferredcontent.min.js
30.06.2021  12:50           150 161 dialog.min.js
30.06.2021  13:27            65 468 divider.min.js
30.06.2021  12:50           199 720 dropdown.min.js
30.06.2021  12:51           130 223 editor.min.js
30.06.2021  12:51            71 946 fieldset.min.js
30.06.2021  12:53            77 397 fileupload.min.js
30.06.2021  12:53            58 767 fullcalendar.min.js
30.06.2021  12:57           118 275 galleria.min.js
30.06.2021  12:57            63 975 inlinemessage.min.js
30.06.2021  12:58            67 726 inplace.min.js
30.06.2021  13:03           133 235 inputmask.min.js
30.06.2021  13:03           173 293 inputnumber.min.js
30.06.2021  13:04            63 437 inputswitch.min.js
30.06.2021  13:28            54 792 inputtext.min.js
30.06.2021  13:04           105 823 knob.min.js
30.06.2021  13:04           124 223 listbox.min.js
30.06.2021  13:05           127 048 megamenu.min.js
30.06.2021  13:05           108 196 menu.min.js
30.06.2021  13:06           119 471 menubar.min.js
30.06.2021  13:07            70 885 message.min.js
30.06.2021  13:07           207 108 multiselect.min.js
30.06.2021  13:07           124 208 orderlist.min.js
30.06.2021  13:07            96 068 organizationchart.min.js
30.06.2021  13:08            51 618 overlayeventbus.min.js
30.06.2021  13:08           108 105 overlaypanel.min.js
30.06.2021  13:08           119 874 paginator.min.js
30.06.2021  13:09            71 809 panel.min.js
30.06.2021  13:09           114 763 panelmenu.min.js
30.06.2021  13:10           112 915 password.min.js
30.06.2021  13:29           170 318 picklist.min.js
30.06.2021  13:30            70 256 progressbar.min.js
30.06.2021  13:10            63 880 progressspinner.min.js
30.06.2021  13:10            65 233 radiobutton.min.js
30.06.2021  13:10            66 511 rating.min.js
30.06.2021  13:11            58 630 ripple.min.js
30.06.2021  13:11            51 902 row.min.js
30.06.2021  13:12            99 436 scrollpanel.min.js
30.06.2021  13:12            76 324 scrolltop.min.js
30.06.2021  13:12            74 316 selectbutton.min.js
30.06.2021  13:12            91 935 sidebar.min.js
30.06.2021  13:13            61 771 skeleton.min.js
30.06.2021  13:13            93 931 slider.min.js
30.06.2021  13:13            67 421 splitbutton.min.js
30.06.2021  13:14           110 047 splitter.min.js
30.06.2021  13:14            54 738 splitterpanel.min.js
30.06.2021  13:14            78 029 steps.min.js
30.06.2021  13:14            83 237 tabmenu.min.js
30.06.2021  13:15            52 653 tabpanel.min.js
30.06.2021  13:15            83 216 tabview.min.js
30.06.2021  13:15            62 341 tag.min.js
30.06.2021  13:16            75 021 terminal.min.js
30.06.2021  13:16            51 618 terminalservice.min.js
30.06.2021  13:16            64 372 textarea.min.js
30.06.2021  13:16           132 609 tieredmenu.min.js
30.06.2021  13:17            73 286 timeline.min.js
30.06.2021  13:17            91 272 toast.min.js
30.06.2021  13:17            51 596 toasteventbus.min.js
30.06.2021  13:17            54 165 toastservice.min.js
30.06.2021  13:18            63 244 togglebutton.min.js
30.06.2021  13:18            57 018 toolbar.min.js
30.06.2021  13:18            71 223 tooltip.min.js
30.06.2021  13:18           168 536 tree.min.js
30.06.2021  13:18           141 710 treeselect.min.js
30.06.2021  13:19           379 775 treetable.min.js
30.06.2021  13:18            63 580 tristatecheckbox.min.js
30.06.2021  13:06            53 061 useconfirm.min.js
30.06.2021  13:05            53 017 usetoast.min.js
30.06.2021  13:05           164 927 utils.min.js
'''


def _get_file_list(text):
    return [line.strip().split()[4][:-7] for line in text.split('\n') if line]


def fetch_file(url, filename, dst_dir):
    res = requests.request('GET', url)
    if res.status_code == 200:
        open(os.path.join(dst_dir, filename), 'wb').write(res.content)


def fetch_primevue_libjs(version='3.7.1', files_list=(), dst_dir='.'):
    if os.path.exists(dst_dir):
        for file_name in files_list:
            fetch_file(f'https://unpkg.com/primevue@{version}/{file_name}/{file_name}.min.js', f'{file_name}.min.js',
                       dst_dir)
            fetch_file(f'https://unpkg.com/primevue@{version}/{file_name}/{file_name}.js', f'{file_name}.js',
                       dst_dir)


def fetch_file_list(path: str, file_list=None, ignore_ends=('.cjs.js', '.cjs.min.js', '.esm.js', '.esm.min.js')):
    print(path)
    res = requests.request('GET', f'https://unpkg.com/{path}')
    file_list = file_list if file_list is not None else []
    if res.status_code == 200:
        soap = bs4.BeautifulSoup(res.text, features="html.parser")
        table_rows = soap.find_all('tr')

        for row in table_rows:
            tds = row.find_all('td', class_='css-1iilqp9')
            if tds:
                link = tds[0].find('a')
                if link:
                    href = link.attrs['href']
                    if href.endswith('/') and href != '../':
                        file_list = fetch_file_list(f'{path}{href}', file_list, ignore_ends)
                    elif href.endswith('.js'):
                        if any([href.endswith(suffix) for suffix in ignore_ends]):
                            # print(f'{href} - script ignored')
                            continue
                        else:
                            file_list.append((href, path))
                    elif href.endswith('.css'):
                        file_list.append((href, path))
                    elif href.endswith('.woff'):
                        file_list.append((href, path))
                    elif href.endswith('.woff2'):
                        file_list.append((href, path))
                    else:
                        #print(f'{href} - ignored')
                        continue
    return file_list


def fetch_primevue_libjs2(lin_name='primevue', version='3.7.1', dst_dir='.'):
    lib_dir = f'{lin_name}_{version}'
    lib_url = f'{lin_name}@{version}/'
    path = os.path.join(dst_dir, lib_dir)
    if not os.path.exists(path):
        os.mkdir(path)
    file_safe_path = os.path.join(path, 'js')
    if not os.path.exists(file_safe_path):
        os.mkdir(file_safe_path)
    if os.path.exists(path) and os.path.exists(file_safe_path):
        file_list = fetch_file_list(lib_url)
        for name, url in file_list:
            if name.endswith('.js'):
                if os.path.exists(file_safe_path):
                    fetch_file(f'https://unpkg.com/{url}{name}', name, file_safe_path)
            else:
                if url.startswith(lib_url):
                    save_path = url[len(lib_url):]
                    path_elements = save_path.split('/')
                    save_path = os.path.join(path, *path_elements)
                    if not os.path.exists(save_path):
                        if len(path_elements) == 1:
                            os.mkdir(save_path)
                        else:
                            current_path = path
                            for path_element in path_elements:
                                current_path = os.path.join(current_path, path_element)
                                if not os.path.exists(current_path):
                                    os.mkdir(current_path)
                    if os.path.exists(save_path):
                        fetch_file(f'https://unpkg.com/{url}{name}', name, save_path)


if __name__ == '__main__':
    # list_files = _get_file_list(file_list_from_dir)
    # print(list_files)
    # fetch_primevue_libjs(files_list=list_files, dst_dir='./js/')
    fetch_primevue_libjs2()
