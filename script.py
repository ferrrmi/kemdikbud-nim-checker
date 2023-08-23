import requests
from tabulate import tabulate

def get_second_api_response(data_first_api):
    hash_value = data_first_api['mahasiswa'][0]['website-link'].split('/')[-1]
    
    url = f'https://api-frontend.kemdikbud.go.id/detail_mhs/{hash_value}'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://pddikti.kemdikbud.go.id',
        'Referer': 'https://pddikti.kemdikbud.go.id/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': 'Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows'
    }
    response_second_api = requests.get(url, headers=headers)
    return response_second_api

def get_first_api_response(kata_kunci):
    url = f'https://api-frontend.kemdikbud.go.id/hit_mhs/{kata_kunci}'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://pddikti.kemdikbud.go.id',
        'Referer': 'https://pddikti.kemdikbud.go.id/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': 'Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows'
    }
    response_first_api = requests.get(url, headers=headers)
    return response_first_api

def get_semester_info(semester_code):
    year = semester_code[:4]
    semester_type = semester_code[-1]
    
    semester_label = f"{year} "
    if semester_type == "1":
        semester_label += "Ganjil"
    elif semester_type == "0":
        semester_label += "Genap"
    else:
        semester_label += "Unknown"
    
    return semester_label

def main():
    try:
        # start script
        print("\n--- NIM Checker by KEMDIKBUD API ---\n")
        
        # input NIM disini
        kata_kunci = input("Input Kata Kunci (Nama Lengkap atau NIM)\n> ")
        
        # if logic NIM is null / null input
        if kata_kunci == "":
            print("\nData yang anda input kosong!")    
        
        # else logic if kata_kunci
        else:
            response_first_api = get_first_api_response(kata_kunci)
            if response_first_api.status_code == 200:
                data_first_api = response_first_api.json()  # Convert response to JSON
                
                # if kata kunci tidak ditemukan
                if data_first_api['mahasiswa'][0]['text'] == f"Cari kata kunci {kata_kunci} pada Data Mahasiswa":
                    print(f"\nkata kunci {kata_kunci} tidak ditemukan!")
                else:
                    # lempar data response 1st api ke 2nd api untuk di proses dan ambil lagi hasil response 2nd api
                    response_second_api = get_second_api_response(data_first_api)  # Pass the JSON data
                    
                    # start logic for 2nd api response into result
                    if response_second_api.status_code == 200:
                        data_second_api = response_second_api.json()  # Convert response to JSON
                        # print(data_second_api)
                        
                        # gender / jenis kelamin
                        gender = ""
                        if data_second_api['dataumum']['jk'] == "L":
                            gender = "Laki-Laki"
                        elif data_second_api['dataumum']['jk'] == "P":
                            gender = "Perempuan"
                        else:
                            gender = "Unknown Gender"
                        
                        # nomor_ijazah
                        if data_second_api['dataumum']['no_seri_ijazah'] is None:
                            nomor_ijazah = "-"
                        elif data_second_api['dataumum']['no_seri_ijazah'] == "":
                            nomor_ijazah = "-"
                        else:
                            nomor_ijazah = data_second_api['dataumum']['no_seri_ijazah']
                        
                        # status_mahasiswa
                        if data_second_api['dataumum']['ket_keluar'] is None:
                            status_mahasiswa = "Belum Lulus"
                        elif data_second_api['dataumum']['ket_keluar'] == "":
                            status_mahasiswa = "-"
                        else:
                            status_mahasiswa = data_second_api['dataumum']['ket_keluar']
                            
                        # Determine semester info
                        semester_code = data_second_api['dataumum']['mulai_smt']
                        semester_info = get_semester_info(semester_code)
                        # print(f"Semester: {semester_info}")
                        
                        #table data mahasiswa
                        table_data = [
                            ["Nama", data_second_api["dataumum"]["nm_pd"]],
                            ["Jenis Kelamin", gender],
                            ["Nomor Induk Mahasiswa", data_second_api["dataumum"]["nipd"]],
                            ["Perguruan Tinggi", data_second_api["dataumum"]["namapt"]],
                            ["Jenjang", data_second_api["dataumum"]["namajenjang"]],
                            ["Program Studi", data_second_api["dataumum"]["namaprodi"]],
                            ["Semester Awal", semester_info],
                            ["Status Awal Mahasiswa", data_second_api["dataumum"]["nm_jns_daftar"]],
                            ["Status Mahasiswa Saat ini", status_mahasiswa],
                            ["Nomor Ijazah", nomor_ijazah]
                        ]
                        
                        # fill table with table data
                        table = tabulate(table_data, headers=["Informasi Mahasiswa:", ""], tablefmt="plain")
                        
                        #print isi table
                        print(f"\n{table}\n\n*jika pencarian menggunakan nama tidak sesuai, gunakan nomor induk mahasiswa*")
                    else:
                        print('\nRequest 2nd api failed with status code:', response_second_api.status_code)
            else:
                print('\nRequest 1st api failed with status code:', response_first_api.status_code)
    # keyboard interrupt
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    # exception awal    
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()