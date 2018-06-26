# PyTorrent

Implementação de um programa para compartilhamento de arquivos ponto-a-ponto (P2P) usando o protocolo BitTorrent Protocol: BTP/1.0

A pasta example.torrent contem arquivos de teste. O arquivo onlyonefile.torrent eh apenas uma foto para torrnet. O arquivo 'text.decode' eh o que esta funcionando para o decode.

O decode e o bencode do padrao BENCODE esta 100% funcionando. Para usar em qualquer arquivo .torrent: from Decode import DBdecode -> Decode('path/namefile').decodeFullFile()

Adições dos recursos (mais antigos por ultimo):

- Recebendo lista de Peers do Tracker via UDP.

- Recebendo lista de Peers do Tracker via TCP.

- Obtendo SHA1 da 'info'.

- Bencode encodificando um objecto.

- Requisitando ao Tracker a lista de peers.

- Mecanismo de geração do peer id e recuperação do peer id.

- Implementação da interface para abrir arquivos e mostrando as informações de torrents.

- Verificando a validade dos arquivos com base nas suas respectivas chaves.

- Implementação da interface principal do programa.

- Implementado o Decode para obter os SHA-1 das peças do torrent. DECODE BENCODE 100% works.

- Implementaçao do Decode apenas para arquivos normais.

- Decode completo para arquivos UTF8.
