import requests
import datetime

import discord

from thefuzz import process


class CurrencyConverter():
    def __init__(self):
        url = 'https://api.exchangerate-api.com/v4/latest/USD'
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']
        self.lastUpdateInt = self.data['time_last_updated']
        self.lastUpdate = datetime.datetime.fromtimestamp(self.lastUpdateInt)

        self.allCountries = [
            ["Afghanistan", "AFN Afghan Afghani", "AF", "AFN"],
            ["Albania", "ALL Albanian lek", "AL", "ALL"],
            ["Algeria", "DZD Algerian dinar", "DZ", "DZD"],
            ["American Samoa", "USD US dollar", "AS", "USD"],
            ["Andorra", "EUR Euro", "AD", "EUR"],
            ["Angola", "AOA Angolan kwanza", "AO", "AOA"],
            ["Anguilla", "XCD East Caribbean dollar", "AI", "XCD"],
            ["Antigua and Barbuda", "XCD East Caribbean dollar", "AG", "XCD"],
            ["Argentina", "ARS Argentine peso", "AR", "ARS"],
            ["Armenia", "AMD Armenian dram", "AM", "AMD"],
            ["Aruba", "AWG Aruban guilder", "AW", "AWG"],
            ["Australia", "AUD Australian dollar", "AU", "AUD"],
            ["Austria", "EUR Euro", "AT", "EUR"],
            ["Azerbaijan", "AZN New azerbaijani Manat", "AZ", "AZN"],
            ["Bahamas", "BSD Bahamian dollar", "BS", "BSD"],
            ["Bahrain", "BHD Bahraini dinar", "BH", "BHD"],
            ["Banglades", "BDT Bangladeshi taka", "BD", "BDT"],
            ["Barbados", "BBD Barbados dollar", "BB", "BBD"],
            ["Belarus", "BYN Belarusian ruble", "BY", "BYN"],
            ["Belgium", "EUR Euro", "BE", "EUR"],
            ["Belize", "BZD Belize dollar", "BZ", "BZD"],
            ["Benin", "XOF CFA Franc BCEAO", "BJ", "XOF"],
            ["Bermuda", "BMD Bermudian dollar", "BM", "BMD"],
            ["Bhutan", "BTN Bhutanese ngultrum", "BT", "BTN"],
            ["Bolivia", "BOB Boliviano", "BO", "BOB"],
            ["Bosnia-Herzegovina", "BAM Convertible mark", "BA", "BAM"],
            ["Botswana", "BWP Botswana pula", "BW", "BWP"],
            ["Bouvet Island", "NOK Norwegian krone", "BV", "NOK"],
            ["Brazil", "BRL Brazilian real", "BR", "BRL"],
            ["British Indian O. Terr.", "GBP Pound sterling", "IO", "GBP"],
            ["British Virgin Islands", "USD US dollar", "VG", "USD"],
            ["Brunei Darussalam", "BND Brunei dollar", "BN", "BND"],
            ["Bulgaria", "BGN Bulgarian lev", "BG", "BGN"],
            ["Burkina Faso", "XOF CFA Franc BCEAO", "BF", "XOF"],
            ["Burundi", "BIF Burundian franc", "BI", "BIF"],
            ["Cambodia", "KHR Cambodian riel", "KH", "KHR"],
            ["Cameroon", "XAF CFA Franc BEAC", "CM", "XAF"],
            ["Canada", "CAD Canadian dollar", "CA", "CAD"],
            ["Cape Verde", "CVE Cape Verde escudo", "CV", "CVE"],
            ["Cayman Islands", "KYD Cayman Islands dollar", "KY", "KYD"],
            ["Central African Rep.", "XAF CFA Franc BEAC", "CF", "XAF"],
            ["Chad", "XAF CFA Franc BEAC", "TD", "XAF"],
            ["Chile", "CLP Chilean peso", "CL", "CLP"],
            ["China", "CNY Chinese yuan renminbi (RMB)", "CN", "CNY"],
            ["Christmas Island", "AUD Australian dollar", "CX", "AUD"],
            ["Cocos (Keeling) Islands", "AUD Australian dollar", "CC", "AUD"],
            ["Colombia", "COP Colombian peso", "CO", "COP"],
            ["Comoros", "KMF Comoro franc", "KM", "KMF"],
            ["Congo (Brazzaville)", "XAF CFA Franc BEAC", "CG", "XAF"],
            ["Cook Islands", "NZD New Zealand dollar", "CK", "NZD"],
            ["Costa Rica", "CRC Costa Rican colon", "CR", "CRC"],
            ["Croatia", "HRK Croatian kuna", "HR", "HRK"],
            ["Cuba", "CUC Cuban convertible Peso", "CU", "CUC"],
            ["Cyprus", "EUR Euro", "CY", "EUR"],
            ["Czech Republic", "CZK Czech koruna", "CS", "CZK"],
            ["Democratic Republic of Congo (Kinshasa-Zaire)",
                "CDF Congolese franc", "CD", "CDF"],
            ["Denmark", "DKK Danish krone", "DK", "DKK"],
            ["Djibouti", "DJF Djiboutian franc", "DJ", "DJF"],
            ["Dominica", "XCD East Caribbean dollar", "DM", "XCD"],
            ["Dominican Republic", "DOP Dominican peso", "DO", "DOP"],
            ["Ecuador", "USD US dollar", "EC", "USD"],
            ["Egypt", "EGP Egyptian pound", "EG", "EGP"],
            ["El Salvador", "SVC Salvadoran colon", "SV", "SVC"],
            ["Eritrea", "ERN Eritrean nakfa", "ER", "ERN"],
            ["Estonia", "EUR Euro", "EE", "EUR"],
            ["Ethiopia", "ETB Ethipian birr", "ET", "ETB"],
            ["European Union", "EUR Euro", "EU", "EUR"],
            ["Falkland Isl.", "FKP Falkland Islands pound", "FK", "FKP"],
            ["Faroe Islands", "DKK Danish krone", "FO", "DKK"],
            ["Fiji", "FJD Fiji dollar", "FJ", "FJD"],
            ["Finland", "EUR Euro", "FI", "EUR"],
            ["France", "EUR Euro", "FR", "EUR"],
            ["France", "EUR Euro", "FR", "EUR"],
            ["French Guiana", "EUR Euro", "GF", "EUR"],
            ["French Polynesia", "XPF French pacific franc", "PF", "XPF"],
            ["French Southern Terr.", "EUR Euro", "TF", "EUR"],
            ["Gabon", "XAF CFA Franc BEAC", "GA", "XAF"],
            ["Gambia", "GMD Gambian dalasi", "GM", "GMD"],
            ["Georgia", "GEL Georgian lari", "GE", "GEL"],
            ["Germany", "EUR Euro", "DE", "EUR"],
            ["Ghana", "GHS Ghanaian Cedi", "GH", "GHS"],
            ["Gibraltar", "GIP Gibraltar pound", "GI", "GIP"],
            ["Great Britain - UK", "GBP Pound sterling", "UK", "GBP"],
            ["Greece", "EUR Euro", "GR", "EUR"],
            ["Greenland (Denmark)", "DKK Danish krone", "GL", "DKK"],
            ["Grenada", "XCD East Caribbean dollar", "GD", "XCD"],
            ["Guadaloupe", "EUR Euro", "GP", "EUR"],
            ["Guam (US)", "USD US dollar", "GU", "USD"],
            ["Guatemala", "GTQ Guatemalan quetzal", "GT", "GTQ"],
            ["Guernsey", "GGP Guernsey Pound", "GG", "GGP"],
            ["Guinea (Conakry)", "GNF Guinean franc", "GN", "GNF"],
            ["Guinea Bissau", "XAF CFA Franc BEAC", "GW", "XAF"],
            ["Guyana", "GYD Guyanese dollar", "GY", "GYD"],
            ["Haiti", "HTG Haitian gourde", "HT", "HTG"],
            ["Heard and McDonald Isl.", "AUD Australian dollar", "HM", "AUD"],
            ["Honduras", "HNL Honduran lempira", "HN", "HNL"],
            ["Hong Kong", "HKD Hong Kong dollar", "HK", "HKD"],
            ["Hungary", "HUF Hungarian forint", "HU", "HUF"],
            ["Iceland", "ISK Icelandic króna", "IS", "ISK"],
            ["India", "INR Indian rupee", "IN", "INR"],
            ["Indonesia", "IDR Indonesian rupiah", "ID", "IDR"],
            ["Iran", "IRR Iranian rial", "IR", "IRR"],
            ["Iraq", "IQD Iraqi dinar", "IQ", "IQD"],
            ["Ireland", "EUR Euro", "IE", "EUR"],
            ["Isle of Man", "IMP Manx pound", "IM", "IMP"],
            ["Israel", "ILS Israeli new shekel", "IL", "ILS"],
            ["Italy", "EUR Euro", "IT", "EUR"],
            ["Ivory Coast", "XOF CFA Franc BCEAO", "CI", "XOF"],
            ["Jamaica", "JMD Jamaican dollar", "JM", "JMD"],
            ["Japan", "JPY Japanese yen", "JP", "JPY"],
            ["Jersey", "JEP Jersey pound", "JE", "JEP"],
            ["Jordan", "JOD Jordanian dinar", "JO", "JOD"],
            ["Kazakhstan", "KZT Kazakhstani tenge", "KZ", "KZT"],
            ["Kenya", "KES Kenyan shilling", "KE", "KES"],
            ["Kiribati", "KID Kiribati dollar", "KI", "KID"],
            ["Kuwait", "KWD Kuwaiti dinar", "KW", "KWD"],
            ["Kyrgyz Republic", "KGS Kyrgyzstani som", "KG", "KGS"],
            ["Laos", "LAK Lao kip", "LA", "LAK"],
            ["Latvia", "EUR Euro", "LV", "EUR"],
            ["Lebanon", "LBP Lebanese pound", "LB", "LBP"],
            ["Lesotho", "LSL Lesotho loti", "LS", "LSL"],
            ["Liberia", "LRD Liberian dollar", "LR", "LRD"],
            ["Libya", "LYD Libyan dinar", "LY", "LYD"],
            ["Liechtenstein", "CHF Swiss franc", "LI", "CHF"],
            ["Lithuania", "LTL Lithuanian litas", "LT", "LTL"],
            ["Luxembourg", "EUR Euro", "LU", "EUR"],
            ["Macau", "MOP Macanese pataca", "MO", "MOP"],
            ["Macedonia", "MKD Macedonian denar", "MK", "MKD"],
            ["Madagascar", "MGA Malagasy ariayry", "MG", "MGA"],
            ["Malawi", "MWK Malawian kwacha", "MW", "MWK"],
            ["Malaysia", "MYR Malaysian ringgit", "MY", "MYR"],
            ["Maldives", "MVR Maldivian rufiyaa", "MV", "MVR"],
            ["Mali", "XOF CFA Franc BCEAO", "ML", "XOF"],
            ["Malta", "EUR Euro", "MT", "EUR"],
            ["Marshall Islands", "USD US dollar", "MH", "USD"],
            ["Martinique", "EUR Euro", "MQ", "EUR"],
            ["Mauritania", "MRU Mauritanian ouguiya", "MR", "MRU"],
            ["Mauritius", "MUR Mauritian rupee", "MU", "MUR"],
            ["Mayotte", "EUR Euro", "YT", "EUR"],
            ["Mexico", "MXN Mexican peso", "MX", "MXN"],
            ["Micronesia", "USD US dollar", "FM", "USD"],
            ["Moldova", "MDL Moldovan leu", "MD", "MDL"],
            ["Monaco", "EUR Euro", "MC", "EUR"],
            ["Mongolia", "MNT Mongolian tugrik", "MN", "MNT"],
            ["Montenegro", "EUR Euro", "ME", "EUR"],
            ["Montserrat", "XCD East Caribbean dollar", "MS", "XCD"],
            ["Morocco", "MAD Moroccan dirham", "MA", "MAD"],
            ["Mozambique", "MZN Mozambican metical", "MZ", "MZN"],
            ["Myanmar", "MMK Myanma kyat", "MM", "MMK"],
            ["Namibia", "NAD Namibian dollar", "NA", "NAD"],
            ["Nauru", "AUD Australian dollar", "NR", "AUD"],
            ["Nepal", "NPR Nepalese rupee", "NP", "NPR"],
            ["Netherland Antilles", "ANG Netherlands Antillean guilder",
                "AN", "ANG"],
            ["Netherlands", "EUR Euro", "NL", "EUR"],
            ["New Caledonia", "XPF French pacific franc", "NC", "XPF"],
            ["New Zealand", "NZD New Zealand dollar", "NZ", "NZD"],
            ["Nicaragua", "NIO Nicaraguan córdoba", "NI", "NIO"],
            ["Niger", "XOF CFA Franc BCEAO", "NE", "XOF"],
            ["Nigeria", "NGN Nigerian naira", "NG", "NGN"],
            ["Niue", "NZD New Zealand dollar", "NU", "NZD"],
            ["Norfolk Island", "AUD Australian dollar", "NF", "AUD"],
            ["North Korea", "KPW North Korean won", "KP", "KPW"],
            ["Northern Mariana Isl.", "USD US dollar", "MP", "USD"],
            ["Norway", "NOK Norwegian krone", "NO", "NOK"],
            ["Oman", "OMR Omani rial", "OM", "OMR"],
            ["Pakistan", "PKR Pakistani rupee", "PK", "PKR"],
            ["Palau", "USD US dollar", "PW", "USD"],
            ["Palestine", "ILS Israeli new shekel", "PS", "ILS"],
            ["Panama", "PAB Panamanian balboa", "PA", "PAB"],
            ["Papua New Guinea", "PGK Papua New Guinean kina", "PG", "PGK"],
            ["Paraguay", "PYG Paraguayan guaraní", "PY", "PYG"],
            ["Peru", "PEN Peruvian nuevo sol", "PE", "PEN"],
            ["Philippines", "PHP Philippine peso", "PH", "PHP"],
            ["Pitcairn", "NZD New Zealand dollar", "PN", "NZD"],
            ["Poland", "PLN Polish zloty", "PL", "PLN"],
            ["Portugal", "EUR Euro", "PT", "EUR"],
            ["Puerto Rico", "USD US dollar", "PR", "USD"],
            ["Qatar", "QAR Qatari riyal", "QA", "QAR"],
            ["Reunion", "EUR Euro", "RE", "EUR"],
            ["Romania", "RON Romanian new Leu", "RO", "RON"],
            ["Russian Federation", "RUB Russian ruble", "RU", "RUB"],
            ["Rwanda", "RWF Rwandan franc", "RW", "RWF"],
            ["Saint Lucia", "XCD East Caribbean dollar", "LC", "XCD"],
            ["Saint Pierre and Miquelon", "EUR Euro", "PM", "EUR"],
            ["San Marino", "EUR Euro", "SM", "EUR"],
            ["Saudi Arabia", "SAR Saudi riyal", "SA", "SAR"],
            ["Senegal", "XOF CFA Franc BCEAO", "SN", "XOF"],
            ["Serbia", "RSD Serbian dinar", "RS", "RSD"],
            ["Seychelles", "SCR Seychelles rupee", "SC", "SCR"],
            ["Sierra Leone", "SLL Sierra Leonean leone", "SL", "SLL"],
            ["Singapore", "SGD Singapore dollar", "SG", "SGD"],
            ["Sint Maarten (Dutch part)", "ANG Netherlands Antillean guilder",
                "SX", "ANG"],
            ["Slovakia", "EUR Euro", "SK", "EUR"],
            ["Slovenia", "EUR Euro", "SI", "EUR"],
            ["Solomon Islands", "SBD Solomon Islands dollar", "SB", "SBD"],
            ["Somalia", "SOS Somali shilling", "SO", "SOS"],
            ["South Africa", "ZAR South African rand", "ZA", "ZAR"],
            ["South Georgia and South Sandwich Islands",
                "GBP Pound sterling", "GS", "GBP"],
            ["South Korea", "KRW South Korean won", "KR", "KRW"],
            ["South Sudan", "SSP South Sudanese Pound", "SS", "SSP"],
            ["Soviet Union", "RUB Russian ruble", "RU", "RUB"],
            ["Spain", "EUR Euro", "ES", "EUR"],
            ["Sri Lanka", "LKR Sri Lankan rupee", "LK", "LKR"],
            ["St. Helena", "SHP Saint Helena pound", "SH", "SHP"],
            ["St. Tome and Principe", "STN São Tomé dobra", "ST", "STN"],
            ["St.Kitts Nevis Anguilla", "XCD East Caribbean dollar",
                "KN", "XCD"],
            ["St.Vincent and Grenadines", "XCD East Caribbean dollar",
                "VC", "XCD"],
            ["Sudan", "SDG Sudanese pound", "SD", "SDG"],
            ["Suriname", "SRD Surinamese dollar", "SR", "SRD"],
            ["Svalbard and Jan Mayen Is", "NOK Norwegian krone", "SJ", "NOK"],
            ["Swaziland", "SZL Swazi lilangeni", "SZ", "SZL"],
            ["Sweden", "SEK Swedish krona", "SE", "SEK"],
            ["Switzerland", "CHF Swiss franc", "CH", "CHF"],
            ["Syria", "SYP Syrian pound", "SY", "SYP"],
            ["Taiwan", "TWD New Taiwan dollar", "TW", "TWD"],
            ["Tajikistan", "TJS Tajikistani somoni", "TJ", "TJS"],
            ["Tanzania", "TZS Tanzanian shilling", "TZ", "TZS"],
            ["Thailand", "THB Thai baht", "TH", "THB"],
            ["Timor-Leste", "USD US dollar", "TL", "USD"],
            ["Togo", "XOF CFA Franc BCEAO", "TG", "XOF"],
            ["Tokelau", "NZD New Zealand dollar", "TK", "NZD"],
            ["Tonga", "TOP Tongan pa'anga", "TO", "TOP"],
            ["Trinidad and Tobago", "TTD Trinidad dollar", "TT", "TTD"],
            ["Tunisia", "TND Tunisian dinar", "TN", "TND"],
            ["Turkey", "TRY Turkish lira", "TR", "TRY"],
            ["Turkmenistan", "TMT Turkmenistani new manat", "TM", "TMT"],
            ["Turks and Caicos Islands", "USD US dollar", "TC", "USD"],
            ["Tuvalu", "AUD Australian dollar", "TV", "AUD"],
            ["Uganda", "UGX Ugandan shilling", "UG", "UGX"],
            ["Ukraine", "UAH Ukrainian hryvnia", "UA", "UAH"],
            ["United Arab Emirates", "AED UAE dirham", "AE", "AED"],
            ["United States", "USD US dollar", "US", "USD"],
            ["Uruguay", "UYU Urugayan peso", "UY", "UYU"],
            ["US Minor outlying Isl.", "USD US dollar", "UM", "USD"],
            ["US Virgin Islands", "USD US dollar", "VI", "USD"],
            ["Uzbekistan", "UZS Uzbekitan som", "UZ", "UZS"],
            ["Vanuatu", "VUV Vanuatu vatu", "VU", "VUV"],
            ["Vatican City State", "EUR Euro", "VA", "EUR"],
            ["Venezuela", "VES sovereign bolivar", "VE", "VES"],
            ["Vietnam", "VND Vietnamese đồng", "VN", "VND"],
            ["Wallis and Futuna Islands", "XPF French pacific franc",
                "WF", "XPF"],
            ["Western Sahara", "MAD Moroccan dirham", "EH", "MAD"],
            ["Western Samoa", "WST Samoan tala", "WS", "WST"],
            ["Yemen", "YER Yemeni rial", "YE", "YER"],
            ["Yugoslavia", "YUN Yugoslav dinar", "YU", "YUN"],
            ["Zambia", "ZMW Zambian kwacha", "ZM", "ZMW"],
            ["Zimbabwe", "ZWL Zimbabwe dollar", "ZW", "ZWL"]]

        currencies_codes = []
        for i, item in enumerate(self.allCountries):
            currencies_codes.append(item[3])

        text = sorted(list(self.currencies.keys()))
        texts = []
        texts_msg = ''
        for item in text:
            try:
                if (len(texts_msg) >= 4096):
                    texts.append(texts_msg)
                    texts_msg = ''
                texts_msg += f'{item} {self.allCountries[currencies_codes.index(item)][0]}\n'
            except ValueError:  # Didn't find country
                pass
        texts.append(texts_msg)
        embeds = []
        for idx, item in enumerate(texts):
            embeds.append(
                discord.Embed(
                    type='rich',
                    title=f'💰🌏 List of currencies [{idx}/{len(embeds)}] 🌏💰',
                    colour=0x78FF78, description=item,
                )
            )
        self.embedsOfCurrencies = embeds

    def getFromList(self, currency):
        countries = []
        currencies = []
        codes = []
        currencies_codes = []

        for i, item in enumerate(self.allCountries):
            countries.append(item[0])
            currencies.append(item[1])
            codes.append(item[2])
            currencies_codes.append(item[3])

        i = currencies_codes.index(currency)

        return [countries[i], currencies[i], codes[i], currencies_codes[i]]

    def getCurrency(self, text):
        search = text
        answers = []

        countries = []
        currencies = []
        codes = []
        currencies_codes = []

        for i, item in enumerate(self.allCountries):
            countries.append(item[0])
            currencies.append(item[1])
            codes.append(item[2])
            currencies_codes.append(item[3])

        answers.append(process.extractOne(search, countries))
        answers.append(process.extractOne(search, currencies))
        if (len(text) == 2):
            answers.append(process.extractOne(search, codes))
        if (len(text) == 3):
            answers.append(process.extractOne(search, currencies_codes))

        answer = ['', 0]
        for answer_list in answers:
            if answer_list[1] > answer[1]:
                answer = answer_list

        try:
            i = countries.index(answer[0])
        except ValueError:
            try:
                i = currencies.index(answer[0])
            except ValueError:
                try:
                    i = codes.index(answer[0])
                except ValueError:
                    i = currencies_codes.index(answer[0])

        return [countries[i], currencies[i], codes[i], currencies_codes[i]]

    def convert(self, from_currency, to_currency, amount=1):
        if (from_currency != 'USD'):
            try:
                amount = amount / self.currencies[from_currency]
            except KeyError:
                return -1
        try:
            amount = round(amount * self.currencies[to_currency], 2)
        except KeyError:
            return -2
        return amount


def main():
    converter = CurrencyConverter()
    searched = converter.getCurrency('Peso')
    print(searched)


if __name__ == '__main__':
    main()
