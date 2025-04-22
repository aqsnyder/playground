import pandas as pd

def parse_netlist_v5(netlist_path):
    components = []
    nets = []

    with open(netlist_path, 'r') as file:
        lines = file.readlines()

    # Parse components
    parsing_components = False
    component = {}
    for line in lines:
        if line.strip().startswith("(components"):
            parsing_components = True
        elif parsing_components:
            if line.strip().startswith("(comp "):
                component = {}  # Start a new component
            elif line.strip().startswith("(ref "):
                component["Reference"] = line.split('"')[1]  # Extract reference
            elif line.strip().startswith("(value "):
                component["Value"] = line.split('"')[1]  # Extract value
            elif line.strip().startswith("(footprint "):
                component["Footprint"] = line.split('"')[1]  # Extract footprint
            elif line.strip().startswith("(datasheet "):
                component["Datasheet"] = line.split('"')[1]  # Extract datasheet
            elif line.strip().startswith("(description "):
                component["Description"] = line.split('"', 1)[1].rsplit('"', 1)[0]  # Extract description
            elif line.strip().startswith("(property (name \"Sheetname\")"):
                component["Sheetname"] = line.split('"')[3]  # Extract sheet name
            elif line.strip().startswith(")"):  # End of component
                if component:
                    components.append(component)
            elif line.strip().startswith(")"):  # End of components section
                parsing_components = False

    # Parse nets
    parsing_nets = False
    current_net = None
    for line in lines:
        if line.strip().startswith("(net "):
            # Start a new net
            current_net = line.strip().split('"')[1]  # Extract net name
        elif line.strip().startswith("(node "):
            try:
                # Extract node details
                parts = line.strip().split('"')
                ref = parts[1]  # Component reference
                pin = parts[3]  # Pin number
                nets.append({
                    "Net": current_net,
                    "Component": ref,
                    "Pin": pin,
                })
            except IndexError:
                print(f"Warning: Skipping malformed line: {line.strip()}")
        elif line.strip().startswith(")"):  # End of nets section
            parsing_nets = False

    return components, nets


def save_to_excel(components, nets, output_path):
    # Convert data to pandas DataFrames
    components_df = pd.DataFrame(components)
    nets_df = pd.DataFrame(nets)

    # Save to Excel with multiple sheets
    with pd.ExcelWriter(output_path) as writer:
        if not components_df.empty:
            components_df.to_excel(writer, sheet_name="Components", index=False)
        else:
            print("No components found!")
        if not nets_df.empty:
            nets_df.to_excel(writer, sheet_name="Nets", index=False)
        else:
            print("No nets found!")

# Paths for the netlist and output Excel file
netlist_path = "xbee_dev_board.net"  # Replace with your actual file path
output_path = "Pin_Connections.xlsx"

# Parse the netlist and generate Excel
try:
    components, nets = parse_netlist_v5(netlist_path)
    save_to_excel(components, nets, output_path)
    print(f"Pin connections saved successfully to {output_path}")
except Exception as e:
    print(f"Error: {e}")
