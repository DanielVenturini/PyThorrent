# PyThorrent

Implementação de um programa para compartilhamento de arquivos ponto-a-ponto (P2P) usando o protocolo BitTorrent Protocol: BTP/1.0

A pasta example.torrent contem arquivos de teste. O arquivo onlyonefile.torrent eh apenas uma foto para torrnet. O arquivo 'text.decode' eh o que esta funcionando para o decode.

O decode do padrao BENCODE esta 100% funcionando. Para usar em qualquer arquivo .torrent: from BDecode import DBdecode -> BDecode('path/namefile').decodeFullFile()

Adições dos recursos (mais antigos por ultimo):

- Implementado o Decode para obter os SHA-1 das peças do torrent. DECODE BENCODE 100% works.

- Implementaçao do Decode apenas para arquivos normais.

- Decode completo para arquivos UTF8
