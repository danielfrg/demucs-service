# Demucs - Music Source Separation

The Demucs is a free service that takes a song and splits it into 4 different tracks:
drums, bass, other and vocals.

[![demucs-service](/docs/public/images/demucs-web.png)](https://demucs.danielfrg.com)

## Example

Original:

<audio controls="">
    <source src="/docs/public/sample/mixture.mp3" type="audio/mp3">
</audio>

Output:

<table>
<tbody>
    <tr>
        <th>Instrument</th>
        <th>Audio</th>
    </tr>
    <tr>
        <td>Drums</td>
        <td><audio controls=""><source src="/docs/public/sample/drums.mp3" type="audio/mp3"></audio></td>
    </tr>
    <tr>
        <td>Bass</td>
        <td><audio controls=""><source src="/docs/public/sample/bass.mp3" type="audio/mp3"></audio></td>
    </tr>
    <tr>
        <td>Other</td>
        <td><audio controls=""><source src="/docs/public/sample/other.mp3" type="audio/mp3"></audio></td>
    </tr>
    <tr>
        <td>Vocals</td>
        <td><audio controls=""><source src="/docs/public/sample/vocals.mp3" type="audio/mp3"></audio></td>
    </tr>
</tbody>
</table>

## Processing

Any song can be processed but the results might vary depending on the complexity
of the song.

Processing time is about 5 minutes for a 3-4 min song.

## API

We provide a REST API to programmatically convert songs and examples on how to use
it. See: [API](/docs/api).

## Architecture

Take a look on how the service runs on the [Architecture section](/docs/mkarch).
