#!/usr/bin/python3
#  -*- coding: utf-8 -*-
import json
from collections import OrderedDict

import os

from indic_transliteration import xsanscript as sanscript

from jyotisha.names.init_names_auto import init_names_auto
import logging

from jyotisha.panchangam.temporal.festival import read_old_festival_rules_dict

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
)



CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

if __name__ == '__main__':
    NAMES = init_names_auto()
    aradhana_rules = read_old_festival_rules_dict(os.path.join(CODE_ROOT, 'panchangam/data/kanchi_aradhana_rules.json'))

    for script in [sanscript.DEVANAGARI, sanscript.IAST]:
        with open(os.path.join(CODE_ROOT, 'kanchi_aradhana_days_%s.md' % script), 'w') as f:
            f.write('## Sri Kanchi Matham Guru Aaradhana Days\n\n')
            f.write('(obtained from [kamakoti.org](http://kamakoti.org/peeth/origin.html#appendix2), ')
            f.write('and corrected using [@kamakoti twitter feed](https://twitter.com/kamakoti)!)\n\n')
            f.write('| # | Jagadguru | Mukti Year (Kali) | Mukti Year Name | Month | Tithi |\n')
            f.write('| - | --------- | ----------------- | --------------- | ----- | ----- |\n')
            for guru in aradhana_rules:
                if guru[:5] == 'kAJcI':
                    name = str(' '.join(guru.split()[3:-1])).replace('-', ' ')
                    num = int(guru.split()[1])
                    kali_year = str(aradhana_rules[guru]['year_start'] - 1)
                    year_name = NAMES['SAMVATSARA_NAMES']['hk'][((int(kali_year) + 12) % 60)]
                else:
                    name = guru[:-9]
                    num = '-'
                    kali_year = '-'
                    year_name = '-'
                tithi = NAMES['TITHI_NAMES']['hk'][aradhana_rules[guru]['angam_number']-1]
                month_name = "UNKNOWN"
                if aradhana_rules[guru]['month_type'] == 'lunar_month':
                    month_name = NAMES['CHANDRA_MASA_NAMES']['hk'][aradhana_rules[guru]['month_number']-1]
                elif aradhana_rules[guru]['month_type'] == 'solar_month':
                    month_name = NAMES['RASHI_NAMES']['hk'][aradhana_rules[guru]['month_number']-1]
                f.write('| %s | %s | %s | %s | %s | %s |\n' %
                        (num, sanscript.transliterate(name, sanscript.HK, script).title(),
                         kali_year, sanscript.transliterate(year_name, sanscript.HK, script), sanscript.transliterate(month_name, sanscript.HK, script), tithi.replace('-', ' ')))
