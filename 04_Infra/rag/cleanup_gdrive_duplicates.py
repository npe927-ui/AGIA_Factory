#!/usr/bin/env python3
"""
Limpieza de duplicados en gdrive del RAG
=========================================
Borra de Chroma los chunks de fuentes gdrive que son copias duplicadas
del mismo libro (múltiples conversiones, múltiples descargas).

Solo borra duplicados SEGUROS — los 87 grupos donde el nombre del fichero
confirma que es el mismo libro/autor con pequeña variación.
Excluye falsos positivos (prefijos ambiguos, módulos de curso distintos).

Uso:
    python3 cleanup_gdrive_duplicates.py --dry-run   # cuenta chunks, no borra
    python3 cleanup_gdrive_duplicates.py             # ejecuta borrado
"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

# Fuentes a BORRAR (duplicados confirmados — versiones inferiores del mismo libro)
SOURCES_TO_DELETE = [
    # === APRENDIZAJE ===
    "gdrive/aprendizaje/a_mind_for_numbers_--_barbara_oakley_--_2014",
    "gdrive/aprendizaje/el_mom_test__cómo_mantener_conversaciones_con_tus_clientes_y_--_rob_fitzpatrick_--_2019",
    "gdrive/aprendizaje/how_to_take_smart_notes_--_sönke_ahrens",
    "gdrive/aprendizaje/how_to_take_smart_notes___one_simple_technique_to_boost_--_sönke_ahrens_nigel_fyfe_--_2nd_edition__revised_and_expanded_edition",
    "gdrive/aprendizaje/make_it_stick___the_science_of_successful_learning_--_peter_c__brown_author_henry_l__roediger_iii_author",

    # === COPYWRITING ===
    "gdrive/copywriting/anotaciones_privadas_de_david_ogilvy___escritos_no_--_david_ogilvy_--_barcelona_d_l__1990",
    "gdrive/copywriting/breakthrough_advertising_--_eugene_schwartz",
    "gdrive/copywriting/10m_-_breakthrough_advertising_-_eugene_schwartz",
    "gdrive/copywriting/el_libro_del_copywriting_-_escribo_para_follar_--_isra_bravo_-_2023",
    "gdrive/copywriting/escribo_porque_me_gusta_ganar_dinero_alienta_spanish_--_isra_bravo_--_alienta_1_2022_--_alienta_editorial",
    "gdrive/copywriting/escribo_porque_me_gusta_ganar_dinero_alienta_spanish_--_bravo_israel_--_alienta_1_2022_--_alienta_editorial",
    "gdrive/copywriting/escribo_porque_me_gusta_ganar_dinero_alienta_spanish_--_isra_bravo_--_alienta_1_2022",
    "gdrive/copywriting/how_to_write_funny__your_serious_step-by-step_blueprint_for_--_scott_dikkers_--_2014",
    "gdrive/copywriting/neurocopywriting_la_ciencia_detrás_de_los_textos_--_rosa_morel",
    "gdrive/copywriting/neurocopywriting_la_ciencia_detrás_de_los_textos_--_rosa_morel_--_2018_--",
    "gdrive/copywriting/neurocopywriting_la_ciencia_detrás_de_los_textos_--_rosa_morel_--_oct_05_2018_--_rosa_morel",
    "gdrive/copywriting/persuasive_copywriting___using_psychology_to_engage_--_maslen_andy_--_kogan_page_london_2015",
    "gdrive/copywriting/persuasive_copywriting__using_psychology_to_engage_--_andy_maslen_--_2015_--_kogan_page",
    "gdrive/copywriting/scientific_advertising_--_claude_c__hopkins_--_2022_--_sanage_publishing_house_llp",
    "gdrive/copywriting/scientific_advertising_-_claude_c__hopkins_-_ultima_edicion-_2010",
    "gdrive/copywriting/storytelling_en_una_semana__autoconocimiento_marca_--_nuñez_antonio_antonio_nuñez_-2011",
    "gdrive/copywriting/the_adweek_copywriting_handbook__the_ultimate_guide_to_--_joseph_sugarman_--_2006",
    "gdrive/copywriting/the_boron_letters_--_gary_halbert",
    "gdrive/copywriting/the_boron_letters_-_ficha_resumen_naca",
    "gdrive/copywriting/the_copywriters_handbook_-_a_step_by_step_guide_to_writing_-_robert_w_bly",
    "gdrive/copywriting/the_copywriters_handbook__a_step-by-step_guide_to_writing_--_robert_w_bly",
    "gdrive/copywriting/trucos_para_escribir_mejor_spanish_edition_--_salas_carlos_--_2013",

    # === EMAIL MARKETING ===
    "gdrive/email_marketing/el_tao_del_email_marketing_-_miguel_vázquez",
    "gdrive/email_marketing/email_marketing_rules__checklists_frameworks_and_150_best_--_chad_s__white_--_2017",
    "gdrive/email_marketing/email_marketing_rules___checklists_frameworks_and_150_best_--_chad_s__white_--_third_edition_north_chareleston_sc_2017_--_createspace_independent",
    "gdrive/email_marketing/maestría_en_email_marketing_-_paquete__email_marketing_--_laguna_helio_--_2016_--_helio_laguna",
    "gdrive/email_marketing/maestría_en_email_marketing_-_paquete__email_marketing_--_laguna_helio_--_2016",

    # === LIDERAZGO ===
    "gdrive/liderazgo/aquí_no_hay_reglas___netflix_y_la_cultura_de_la_reinvención_--_reed_hastings_erin_meyer_efrén_del_valle_peñamil",
    "gdrive/liderazgo/el_arte_de_cautivar__cómo_se_cambian_los_corazones_-guy_kawasaki_-2011",
    "gdrive/liderazgo/las_21_leyes_inquebrantables_del_dinero_spanish_edition_--_brian_tracy_--_2012",
    "gdrive/liderazgo/la_vaca_púrpura_--_seth_godin_--_2008_--_publisher_not_identified_--_isbn13_9788498752311",

    # === MARKETING ===
    "gdrive/marketing/7_secrets_of_marketing_in_a_multi-cultural_world_--_rapaille_gilbert_c__--_1_edition_february_1_2001_--_provo_utah___executive_excellence_pub_",
    "gdrive/marketing/brand_sense___build_powerful_brands_through_touch_taste_--_martin_lindstrom_foreword_by_philip_kotler_--2010",
    "gdrive/marketing/el_ministerio_del_sentido_común_--_martin_lindstrom_--_2021_--_deusto",
    "gdrive/marketing/hable_como_en_ted_--_carmine_gallo",
    "gdrive/marketing/jab_-jab_-jab_-right-hook-signed-edition_-how-to-tell-your-vaynerchuk_-gary",
    "gdrive/marketing/la_molécula_de_la_felicidad_--_zak_paul_j__--_2012",

    # === NEGOCIACION ===
    "gdrive/negociacion/cómo_construir_una_storybrand__clarifica_tu_mensaje_para_que_--_donald_miller_--_2018",
    "gdrive/negociacion/de_entrada_diga_no___start_with_no__the_negotiating_tools_--_jim_camp_--_empresa_activa_barcelona_2004_--_empresa_activa_ediciones_urano_s__a__--_isbn13_9788495787521",
    "gdrive/negociacion/de_entrada_diga_no___start_with_no__the_negotiating_tools_--_jim_camp_--_empresa_activa_barcelona_2004_--_ediciones_urano_--_isbn13_9788495787521",
    "gdrive/negociacion/el_héroe_de_las_mil_caras_--_joseph_campbell_--_1949",
    "gdrive/negociacion/gaps_el_síndrome_psico-intestinal___un_tratamiento_natural_--_natasha_campbell_mcbride_catalina_brümann_--_bookwire_gmbh_s_l__2017",
    "gdrive/negociacion/the-art-of-the-click-_-how-to-harness-the-power-of-glenn-fisher-place-of-publication-not-ide_-_copia",

    # === NEUROCIENCIA ===
    "gdrive/neurociencia/aprende_a_tomar_notas_con_tu_cerebro_digital__leer_es_perder_--_emowe_marcos_--_2024",
    "gdrive/neurociencia/cómo_aprendemos___los_cuatro_pilares_con_los_que_la_--_stanislas_dehaene_maría_josefina_dalessio_--_2020",
    "gdrive/neurociencia/en_defensa_de_la_felicidad_--_ricard_matthieu_--_20022003_--_epublibre",
    "gdrive/neurociencia/estamos_ciegos_--_jürgen_klaric_--_lima_2012_--_biia_internacional_publishing_--_isbn13_9786124151057",
    "gdrive/neurociencia/estamos_ciegos_--_jürgen_klaric_--_lima_2012_--_biia_internacional_publishing",
    "gdrive/neurociencia/estamos_ciegos__pruebas_crudas_de_los_fracasos_billonarios_--_jürgen_klaric",
    "gdrive/neurociencia/liderazgo__el_poder_de_la_inteligencia_emocional_epubs_--_daniel_goleman_goleman_daniel_--_2014",
    "gdrive/neurociencia/neurociencia_del_cuerpo_--_nazareth_castellanos_--_2025_-",
    "gdrive/neurociencia/neurociencia_del_cuerpo_--_nazaret_castellanos_--_2022",
    "gdrive/neurociencia/pensar_rápido_pensar_despacio_--_daniel_kahneman_--_2012",
    "gdrive/neurociencia/reading_in_the_brain___the_new_science_of_how_we_read_--_stanislas_dehaene_--_2011_--_penguin_group_us_--_isbn13_9780143118053",
    "gdrive/neurociencia/thinking_fast_and_slow_-_daniel_kahneman_carol_s_dweck",

    # === PERSUASION ===
    "gdrive/persuasion/así_se_manipula_al_consumidor_--_martin_lindstrom_--_2011_--_epublibre",
    "gdrive/persuasion/brainfluence_gestión_del_conocimiento_--_dooley_roger_--_2015_--_empresa_activa",
    "gdrive/persuasion/cómo_ganar_amigos_e_influir_sobre_las_personas_--_dale_carnegie_--_1936_--_epublibre",
    "gdrive/persuasion/cómo_ganar_amigos_e_influir_sobre_las_personas_--_dale_carnegie_dale_carnegie_--_2012",
    "gdrive/persuasion/cómo_ganar_amigos_e_influir_sobre_las_personas_--_dale_carnegie_--_2007",
    "gdrive/persuasion/nb_-el_poder_de_la_persuasión__cómo_influir_sobre_las_personas_y_--_kurt_mortensen_--_2015",
    "gdrive/persuasion/exactly_what_to_say__the_magic_words_for_influence_and_--_jones_phil_m_--_2017_-",
    "gdrive/persuasion/exactly_what_to_say__the_magic_words_for_influence_and_--_jones_phil_m__--_2017_--_box_of_tricks_publishing",
    "gdrive/persuasion/influence__the_psychology_of_persuasion_--_robert_b__cialdini_phd_--_2009",
    "gdrive/persuasion/influencia__la_psicología_de_la_persuasión_--_robert_b_cialdini",
    "gdrive/persuasion/pre-suasión_-_un_método_revolucionario_para_influir_y_persuadir_-_robert_b_cialdini",

    # === VENTAS ===
    "gdrive/ventas/cómo_piensan_los_consumidores___lo_que_nuestros_clientes_no_--_zaltman_gerald_--_nuevos_paradigmas_barcelona_buenos_aires_bogotá_2004",
    "gdrive/ventas/el_arte_de_cerrar_la_venta__la_clave_para_hacer_más_dinero_--_brian_tracy",
    "gdrive/ventas/hacking_sales__the_playbook_for_building_a_high_velocity_--_max_altschuler_--_2015",
    "gdrive/ventas/poderosas_técnicas_de_negociación_y_ventas_-_cómo_obtener_los_--_anthony_davidson_shaun_aguilar",
    "gdrive/ventas/same_side_selling__how_integrity_and_collaboration_drive_--_ian_altman_jack_quarles_--_2_ps_2014_--_ideapress_publishing_--_isbn13_9781940858074",
    "gdrive/ventas/secretos_del_vendedor_más_rico_del_mundo__diez_consejos_--_dr__camilo_cruz_--_harpercollins_christian_publishing_nashville_2008_--_grupo_nelson",
    "gdrive/ventas/spin_selling__situation_problem_implication_need-payoff_--_neil_rackham_--_1st_edition_1988_--_mcgraw-hill_companies",
    "gdrive/ventas/ventas_101__lo_que_todo_vendedor_profesional_de_éxito_--_zig_ziglar_--_harpercollins_christian_publishing_nashville_2012_--_harpercollins_christian",
    "gdrive/ventas/nb_-_zig_ziglar_ventas__el_manual_definitivo_para_el_vendedor_--_ziglar_zig_-2011",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    import chromadb
    client = chromadb.HttpClient(
        host=os.environ.get("CHROMA_HOST", "localhost"),
        port=int(os.environ.get("CHROMA_PORT", 8000)),
    )
    col = client.get_collection("rag")

    total_before = col.count()
    print(f"\nChunks totales antes: {total_before:,}")
    print(f"Fuentes a borrar    : {len(SOURCES_TO_DELETE)}")
    print(f"Modo                : {'DRY-RUN' if args.dry_run else 'BORRADO REAL'}")
    print("=" * 60)

    total_deleted = 0
    for source in SOURCES_TO_DELETE:
        # Buscar todos los chunks con este source_file
        results = col.get(
            where={"source_file": source},
            include=["metadatas"],
        )
        ids = results["ids"]
        if not ids:
            print(f"  [0 chunks] (no encontrado) {source}")
            continue

        print(f"  [{len(ids):4d} chunks] {'[DRY] ' if args.dry_run else 'BORRANDO '} {source}")
        total_deleted += len(ids)

        if not args.dry_run:
            # Borrar en lotes de 1000
            for i in range(0, len(ids), 1000):
                col.delete(ids=ids[i:i+1000])

    print("=" * 60)
    print(f"Total chunks {'a borrar' if args.dry_run else 'borrados'}: {total_deleted:,}")
    if not args.dry_run:
        total_after = col.count()
        print(f"Chunks totales después: {total_after:,}")
        print(f"Reducción: {total_before - total_after:,} chunks ({(total_before - total_after)/total_before*100:.1f}%)")


if __name__ == "__main__":
    main()
