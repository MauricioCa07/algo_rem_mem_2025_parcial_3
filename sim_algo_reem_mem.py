#!/usr/bin/env python

marcos_libres = [0x0,0x1,0x2]
reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
segmentos =[ ('.text', 0x00, 0x1A),
              ('.data', 0x40, 0x28),
              ('.heap', 0x80, 0x1F),
              ('.stack', 0xC0, 0x22),
             ]

def procesar(segmentos, reqs, marcos_libres):
    page_size = 0x10
    free_frames = list(marcos_libres)
    loaded = {}  
    results = []
    time = 0

    for req in reqs:
        time += 1
        for name, base, limit in segmentos:
            if base <= req < base + limit:
                offset = req - base
                page_idx = offset // page_size
                off_in_page = offset % page_size
                key = (name, page_idx)

                if key in loaded:
                    frame = loaded[key]['frame']
                    loaded[key]['last'] = time
                    action = "Marco ya estaba asignado"
                else:
                    if free_frames:
                        frame = free_frames.pop(0)
                        action = "Marco libre asignado"
                    else:
                        evict_key = None
                        oldest_time = None
                        for k, info in loaded.items():
                            if oldest_time is None or info['last'] < oldest_time:
                                oldest_time = info['last']
                                evict_key = k
                        frame = loaded[evict_key]['frame']
                        del loaded[evict_key]
                        action = "Marco asignado"

                    loaded[key] = {'frame': frame, 'last': time}

                phys = frame * page_size + off_in_page
                results.append((req, phys, action))
                break
        else:
            results.append((req, 0x1FF, "Segmentation Fault"))
            break

    return results

def print_results(results):
    for req, phys, act in results:
        print(f"Req: {req:#04x} Direccion Fisica: {phys:#04x} Acción: {act}")

if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)
