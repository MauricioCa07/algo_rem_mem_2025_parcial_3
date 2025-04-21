#!/usr/bin/env python

marcos_libres = [0x0,0x1,0x2]
reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
segmentos =[ ('.text', 0x00, 0x1A),
             ('.data', 0x40, 0x28),
             ('.heap', 0x80, 0x1F),
             ('.stack', 0xC0, 0x22),
           ]


def procesar(segmentos, reqs, marcos_libres):
    PAGE_SIZE = 16

    loaded_pages = {}      
    lru_list = []          
    free_frames = list(marcos_libres)

    resultados = []
    for req in reqs:
        valido = False
        for _, base, limite in segmentos:
            if base <= req < base + limite:
                valido = True
                break
        if not valido:
            resultados.append((req, 0x1ff, "Segmentation Fault"))
            continue


        page = req // PAGE_SIZE
        offset = req % PAGE_SIZE

        if page in loaded_pages:
            frame = loaded_pages[page]
            accion = "Marco ya estaba asigando"
            lru_list.remove(page)
            lru_list.append(page)
        else:
            if free_frames:
                frame = free_frames.pop()
                loaded_pages[page] = frame
                lru_list.append(page)
                accion = "Marco libre asignado"
            else:
                victim = lru_list.pop(0)
                frame = loaded_pages.pop(victim)
                

                loaded_pages[page] = frame
                lru_list.append(page)
                accion = "Marco asignado"

        direccion_fisica = frame * PAGE_SIZE + offset
        resultados.append((req, direccion_fisica, accion))

    return resultados


def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)

