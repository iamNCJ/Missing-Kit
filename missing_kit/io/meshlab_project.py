def write_meshlab_project(project_file, mesh_file):
    """
    Create a meshlab project file (XML format)
    :param project_file: target project file path
    :param mesh_file: mesh file path
    """
    with open(project_file, 'w') as f:
        f.write(f"""<!DOCTYPE MeshLabDocument>
<MeshLabProject>
 <MeshGroup>
  <MLMesh visible="1" label="{mesh_file}" idInFile="-1" filename="{mesh_file}">
   <MLMatrix44>
1 0 0 0 
0 1 0 0 
0 0 1 0 
0 0 0 1 
</MLMatrix44>
   <RenderingOption pointColor="252 233 79 255" boxColor="234 234 234 255" wireColor="64 64 64 255" pointSize="3" solidColor="192 192 192 255" wireWidth="1">000111000000000000000000000000000000000010100000000100111011110000001101</RenderingOption>
  </MLMesh>
 </MeshGroup>
 <RasterGroup/>
</MeshLabProject>
""")
