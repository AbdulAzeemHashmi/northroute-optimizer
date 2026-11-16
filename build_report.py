"""
Report Generator for NorthRoute Optimizer Assignment 3
Author: Abdul Azeem (24i-2013)
Section: BAI-5A

Generates the required typed PDF report of at most 5 pages.
Follows all rules:
- No en dash (\u2013)
- No em dash (\u2014)
- No emojis
- Clean, simple, easy English
- Includes all problems A through F with working, tables, and figures
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page count.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (pages 2 and above)
        if self._pageNumber > 1:
            self.drawString(
                36, 11 * inch - 26,
                "FAST-NUCES Islamabad | DAA Assignment 3 | Abdul Azeem (24i-2013)"
            )
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(36, 11 * inch - 28, 8.5 * inch - 36, 11 * inch - 28)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(36, 32, 8.5 * inch - 36, 32)
        
        footer_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(8.5 * inch - 36, 20, footer_text)
        self.drawString(36, 20, "Course: Design and Analysis of Algorithms | Section: BAI-5A")
        self.restoreState()


def create_report(output_filename="24i-2013-A3-BAI-5A.pdf"):
    # Target 8.5 x 11 inch with compact margins
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=34,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=17,
        textColor=colors.HexColor("#1a252f"),
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#34495e"),
        spaceAfter=4
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        textColor=colors.HexColor("#1b4f72"),
        spaceBefore=4,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=11.5,
        textColor=colors.HexColor("#2c3e50"),
        spaceBefore=3,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=2
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1e3799"),
        spaceAfter=2
    )

    callout_style = ParagraphStyle(
        "Callout_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1e3799"),
        spaceAfter=2
    )

    story = []

    # =========================================================================
    # PAGE 1: HEADER, PERSONAL PARAMS, PROBLEM A (KNAPSACK)
    # =========================================================================
    header_data = [
        [
            Paragraph("<b>National University of Computer and Emerging Sciences, Islamabad</b>", title_style),
            Paragraph("<b>DAA Assignment 3 Report</b>", ParagraphStyle("RAlign", parent=title_style, alignment=2))
        ],
        [
            Paragraph("Design and Analysis of Algorithms | Fall 2026 | Instructor: Faculty of Computing", subtitle_style),
            Paragraph("<b>Student:</b> Abdul Azeem | <b>Roll No:</b> 24i-2013 | <b>Section:</b> BAI-5A", ParagraphStyle("RAlign2", parent=subtitle_style, alignment=2))
        ]
    ]
    header_table = Table(header_data, colWidths=[330, 210])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1b4f72"), spaceBefore=3, spaceAfter=4))

    # Section 3.1: Personal Parameters
    story.append(Paragraph("1. Personal Parameters Derivation (Section 3.1)", h1_style))
    p_params_text = (
        "Let roll number = <b>24i-2013</b>. The integer formed by the last three digits is <b>s = 13</b>.<br/>"
        "• <b>Van weight capacity (W):</b> W = 15 + (s mod 10) = 15 + (13 mod 10) = 15 + 3 = <b>18</b><br/>"
        "• <b>Target amount for change (T):</b> T = 30 + (s mod 20) = 30 + (13 mod 20) = 30 + 13 = <b>43</b><br/>"
        "• <b>Start hub:</b> index = (s mod 8) = 13 mod 8 = <b>5</b>. Using mapping A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, the start hub is <b>Hub F</b>."
    )
    story.append(Paragraph(p_params_text, body_style))

    # Problem A: 0/1 Knapsack
    story.append(Paragraph("2. Problem A: The Van Loader (0/1 Knapsack)", h1_style))
    
    story.append(Paragraph("<b>A.1 Recurrence Formulation and Base Cases</b>", h2_style))
    rec_text = (
        "Let <i>K(i, w)</i> denote the maximum value achievable considering the first <i>i</i> parcels within capacity limit <i>w</i>.<br/>"
        "• <b>Base Cases:</b> <i>K(0, w) = 0</i> for all <i>w >= 0</i> (no parcels available yields value 0), and <i>K(i, 0) = 0</i> for all <i>i >= 0</i> (zero capacity can hold zero weight).<br/>"
        "• <b>Case 1 (Item too heavy):</b> If <i>wt[i] > w</i>, parcel <i>i</i> cannot fit in capacity <i>w</i>:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>K(i, w) = K(i - 1, w)</b><br/>"
        "• <b>Case 2 (Best of take or do not take):</b> If <i>wt[i] <= w</i>, we take the maximum between excluding parcel <i>i</i> and including parcel <i>i</i>:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>K(i, w) = max( K(i - 1, w), K(i - 1, w - wt[i]) + val[i] )</b>"
    )
    story.append(Paragraph(rec_text, body_style))

    story.append(Paragraph("<b>A.2 Implementations and Verification</b>", h2_style))
    impl_text = (
        "We implemented both top-down memoization (recursive function with state cache) and bottom-up 2D tabulation in Python.<br/>"
        "For van capacity <b>W = 18</b> with the 8 given parcels (P1 to P8):<br/>"
        "• Top-down memoized optimal value: <b>26</b><br/>"
        "• Bottom-up tabulated optimal value: <b>26</b> (Both implementations match exactly)."
    )
    story.append(Paragraph(impl_text, body_style))

    story.append(Paragraph("<b>A.3 Optimal Parcel Selection and Reconstruction Trace</b>", h2_style))
    recon_text = (
        "<b>Tracing method:</b> Starting at table cell <i>(n, W) = (8, 18)</i>, we compare <i>table[i][w]</i> with <i>table[i-1][w]</i>. "
        "If <i>table[i][w] != table[i-1][w]</i>, parcel <i>i</i> was taken; we add it to the solution and deduct its weight: <i>w = w - wt[i]</i>. "
        "If equal, parcel <i>i</i> was skipped, and we move up to row <i>i-1</i>."
    )
    story.append(Paragraph(recon_text, body_style))

    # Table of parcels chosen
    parcel_table_data = [
        ["Parcel", "Weight", "Value", "Decision", "Remaining Capacity w", "Cumulative Value"],
        ["P8 (wt 10, val 15)", "10", "15", "Skip (table[8][18] == table[7][18] == 26)", "w = 18", "0"],
        ["P7 (wt 9, val 13)", "9", "13", "TAKE (table[7][18]=26 != table[6][18]=25)", "w = 18 - 9 = 9", "13"],
        ["P6 (wt 7, val 10)", "7", "10", "TAKE (table[6][9]=13 != table[5][9]=12)", "w = 9 - 7 = 2", "13 + 10 = 23"],
        ["P5, P4, P3, P2", "-", "-", "Skip (weights exceed remaining capacity 2)", "w = 2", "23"],
        ["P1 (wt 2, val 3)", "2", "3", "TAKE (table[1][2]=3 != table[0][2]=0)", "w = 2 - 2 = 0", "23 + 3 = 26"],
        ["Optimal Load Summary", "18", "26", "Chosen: P1, P6, P7 (Total Weight = 18 / 18, Total Value = 26)", "-", "-"]
    ]
    pt_table = Table(parcel_table_data, colWidths=[95, 45, 45, 175, 100, 80])
    pt_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b4f72")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("ALIGN", (4, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e8f8f5")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(pt_table)

    story.append(Paragraph("<b>A.4 Complexity Analysis and Pseudo-Polynomial Nature</b>", h2_style))
    analysis_a_text = (
        "• <b>Time Complexity:</b> O(n * W) = 8 * 18 = 144 table entry computations, each taking O(1) time.<br/>"
        "• <b>Space Complexity:</b> O(n * W) for the 2D tabulation table (can be optimized to O(W) if only the final value is required).<br/>"
        "• <b>Why Pseudo-Polynomial:</b> The algorithm is polynomial in the magnitude of the integer value W, but exponential in the input size. "
        "In computers, the numeric weight W is represented using <i>b = log2(W)</i> bits. Thus, the time complexity is O(n * 2^b), which is exponential with respect to the length of the binary representation."
    )
    story.append(Paragraph(analysis_a_text, body_style))

    # Add page break to guarantee Page 1 boundary
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: PROBLEM B (COIN CHANGE) & PROBLEM C PART 1 (REPRESENTATION)
    # =========================================================================
    story.append(Paragraph("3. Problem B: Making Change (Coin Change)", h1_style))
    
    story.append(Paragraph("<b>B.1 Minimum Coins Bottom-Up DP Formulation</b>", h2_style))
    dp_coin_text = (
        "We are given coin denominations <b>{1, 3, 4, 9}</b> and personal target amount <b>T = 43</b>.<br/>"
        "• <b>Recurrence:</b> Let <i>C(t)</i> be the minimum coins required to make amount <i>t</i>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>C(t) = min { C(t - c) + 1 }</b> for all <i>c in {1, 3, 4, 9}</i> where <i>c <= t</i>.<br/>"
        "• <b>Base Case:</b> <i>C(0) = 0</i> (0 coins are needed to form amount 0).<br/>"
        "• <b>Unreachable Representation:</b> Amounts that cannot be formed are initialized to <b>infinity (float('inf'))</b>.<br/>"
        "• <b>Results for T = 43:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- Minimum number of coins needed: <b>6 coins</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- Actual coins reconstructed: <b>[9, 9, 9, 9, 4, 3]</b> (Sum = 36 + 4 + 3 = 43)."
    )
    story.append(Paragraph(dp_coin_text, body_style))

    story.append(Paragraph("<b>B.2 Greedy Comparison and Counterexample</b>", h2_style))
    greedy_text = (
        "• <b>Greedy Heuristic:</b> Repeatedly take the largest coin <i>c <= remainder</i> until the remainder reaches 0.<br/>"
        "• <b>Execution on T = 43:</b> 43 - 9 = 34; 34 - 9 = 25; 25 - 9 = 16; 16 - 9 = 7; 7 - 4 = 3; 3 - 3 = 0.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Greedy chooses: <b>[9, 9, 9, 9, 4, 3]</b> (Total = 6 coins). Matches the DP minimum for T = 43: <b>True</b>.<br/>"
        "• <b>Counterexample where Greedy Fails:</b> Consider target amount <b>T = 6</b>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b>DP Minimum:</b> <b>2 coins</b>, using two 3-coins <b>[3, 3]</b>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b>Greedy Heuristic:</b> <b>3 coins</b>, greedily selecting 4 first, leaving remainder 2, forcing <b>[4, 1, 1]</b>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b>One-line Reason:</b> Greedy makes a locally optimal choice of the largest coin 4, which leaves an awkward remainder of 2 that requires two 1s, missing the globally optimal combination of two 3s."
    )
    story.append(Paragraph(greedy_text, body_style))

    # Problem C Part 1: Representation
    story.append(Paragraph("4. Problem C: The Road Map (Representation, BFS, DFS)", h1_style))
    story.append(Paragraph("<b>C.1 Graph Representation: Adjacency List and Adjacency Matrix</b>", h2_style))
    story.append(Paragraph(
        "The road network consists of 8 hubs (A to H) and 13 undirected weighted roads. "
        "Roads: A-B (4), A-C (3), B-C (1), B-D (2), C-D (4), C-E (8), D-E (2), D-F (6), E-F (3), E-G (7), F-G (2), F-H (5), G-H (4).",
        body_style
    ))

    # Graph representation table side by side
    adj_list_str = (
        "<b>Adjacency List (Hub: Neighbours):</b><br/>"
        "A: [B(4), C(3)]<br/>"
        "B: [A(4), C(1), D(2)]<br/>"
        "C: [A(3), B(1), D(4), E(8)]<br/>"
        "D: [B(2), C(4), E(2), F(6)]<br/>"
        "E: [C(8), D(2), F(3), G(7)]<br/>"
        "F: [D(6), E(3), G(2), H(5)]<br/>"
        "G: [E(7), F(2), H(4)]<br/>"
        "H: [F(5), G(4)]"
    )

    adj_matrix_data = [
        ["", "A", "B", "C", "D", "E", "F", "G", "H"],
        ["A", "0", "4", "3", "-", "-", "-", "-", "-"],
        ["B", "4", "0", "1", "2", "-", "-", "-", "-"],
        ["C", "3", "1", "0", "4", "8", "-", "-", "-"],
        ["D", "-", "2", "4", "0", "2", "6", "-", "-"],
        ["E", "-", "-", "8", "2", "0", "3", "7", "-"],
        ["F", "-", "-", "-", "6", "3", "0", "2", "5"],
        ["G", "-", "-", "-", "-", "7", "2", "0", "4"],
        ["H", "-", "-", "-", "-", "-", "5", "4", "0"]
    ]
    matrix_table = Table(adj_matrix_data, colWidths=[20] + [22] * 8)
    matrix_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Courier"),
        ("FONTSIZE", (0, 0), (-1, -1), 6.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
    ]))

    rep_comp_data = [
        [Paragraph(adj_list_str, code_style), matrix_table]
    ]
    rep_table = Table(rep_comp_data, colWidths=[270, 270])
    rep_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(rep_table)

    space_text = (
        "• <b>Space Complexity:</b> Adjacency List uses <b>O(V + E)</b> space. Adjacency Matrix uses <b>O(V^2)</b> space.<br/>"
        "• <b>Suitability:</b> For this network, V = 8 and E = 13. The maximum possible edges in a simple graph with 8 vertices is V(V-1)/2 = 28. "
        "Since E is small relative to V^2 (13 << 64), the graph is sparse. The <b>Adjacency List</b> is preferred because it avoids allocating unneeded empty cells and enables O(deg(u)) iteration over adjacent hubs."
    )
    story.append(Paragraph(space_text, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: PROBLEM C PART 2 (BFS, DFS, ANSWERS) & NETWORK FIGURE
    # =========================================================================
    story.append(Paragraph("4. Problem C: BFS, DFS and Graph Structure (Continued)", h1_style))

    story.append(Paragraph("<b>C.2 Breadth-First Search (BFS) Traversal</b>", h2_style))
    bfs_desc = (
        "Starting from personal start hub <b>F</b>, exploring neighbours in strict alphabetical order without edge weights:<br/>"
        "• <b>BFS Visit Order:</b> <b>F -> D -> E -> G -> H -> B -> C -> A</b><br/>"
        "• <b>Hop Distances (Number of roads from Hub F):</b>"
    )
    story.append(Paragraph(bfs_desc, body_style))

    bfs_table_data = [
        ["Hub", "A", "B", "C", "D", "E", "F", "G", "H"],
        ["Hop Distance from F", "3", "2", "2", "1", "1", "0", "1", "1"],
        ["Discovery Step", "Step 7 (via B)", "Step 5 (via D)", "Step 6 (via D)", "Step 1 (via F)", "Step 2 (via F)", "Start (Source)", "Step 3 (via F)", "Step 4 (via F)"]
    ]
    bfs_t = Table(bfs_table_data, colWidths=[120] + [52] * 8)
    bfs_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b4f72")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(bfs_t)

    story.append(Paragraph("<b>C.3 Depth-First Search (DFS) Traversal, Connected Components and Cycles</b>", h2_style))
    dfs_desc = (
        "Starting from <b>F</b>, visiting neighbours alphabetically:<br/>"
        "• <b>DFS Visit Order:</b> <b>F -> D -> B -> A -> C -> E -> G -> H</b><br/>"
        "• <b>Connected Components:</b> Exactly <b>1 component</b>. A single traversal from F discovers all 8 hubs, proving connectivity.<br/>"
        "• <b>Cycle Detection:</b> <b>Graph contains cycles: True</b>. With V = 8 and E = 13, the cyclomatic number is E - V + 1 = 6 independent cycles. "
        "A detected cycle is <b>B -> C -> A -> B</b> (edges B-C, C-A, A-B)."
    )
    story.append(Paragraph(dfs_desc, body_style))

    story.append(Paragraph("<b>C.4 Short Answers with Justifications</b>", h2_style))
    sa_text = (
        "1. <b>Is the graph connected?</b> Yes, because BFS and DFS discover every hub in the network from start hub F in one run (connected components = 1).<br/>"
        "2. <b>Smallest number of roads from hub F to hub H?</b> Exactly <b>1 road</b>, because hub H is directly adjacent to hub F via the road F-H."
    )
    story.append(Paragraph(sa_text, body_style))

    # Add Network Diagram Image
    story.append(Spacer(1, 4))
    if os.path.exists("road_network.png"):
        img = Image("road_network.png", width=7.2 * inch, height=3.3 * inch)
        story.append(img)
        story.append(Paragraph("<i>Figure 1: NorthRoute Road Network with 8 hubs and 13 roads. Red: Start Hub F. Green solid lines: Minimum Spanning Tree (weight = 17). Dashed gray lines: non-MST roads.</i>", callout_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: PROBLEM D (DIJKSTRA) & PROBLEM E (MST)
    # =========================================================================
    story.append(Paragraph("5. Problem D: Shortest Routes (Dijkstra)", h1_style))
    
    story.append(Paragraph("<b>D.1 Dijkstra Implementation and Shortest Distances from Hub F</b>", h2_style))
    dijk_intro = (
        "Dijkstra algorithm computes shortest paths from source hub <b>F</b> to all other hubs using a min-heap priority queue.<br/>"
        "Relaxation rule: if <i>dist[u] + weight(u, v) < dist[v]</i>, then <i>dist[v] = dist[u] + weight(u, v)</i> and <i>prev[v] = u</i>."
    )
    story.append(Paragraph(dijk_intro, body_style))

    dijk_table_data = [
        ["Destination Hub", "Shortest Distance from F", "Predecessor on Path", "Full Shortest Path Sequence"],
        ["Hub A", "11", "B", "F -> E -> D -> B -> A"],
        ["Hub B", "7", "D", "F -> E -> D -> B"],
        ["Hub C", "8", "B", "F -> E -> D -> B -> C"],
        ["Hub D", "5", "E", "F -> E -> D"],
        ["Hub E", "3", "F", "F -> E"],
        ["Hub F (Source)", "0", "None", "F"],
        ["Hub G", "2", "F", "F -> G"],
        ["Hub H", "5", "F", "F -> H"]
    ]
    dt_table = Table(dijk_table_data, colWidths=[95, 115, 110, 220])
    dt_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b4f72")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(dt_table)

    story.append(Paragraph("<b>D.2 Shortest Path from Hub F to Hub H</b>", h2_style))
    p_h_text = (
        "Reconstructing the predecessor chain from H: <i>H -> prev[H] = F</i>.<br/>"
        "• <b>Actual Shortest Path:</b> <b>F -> H</b><br/>"
        "• <b>Shortest Path Distance:</b> <b>5</b> (Direct road F-H has length 5, which beats the alternative route F-G-H of length 2 + 4 = 6)."
    )
    story.append(Paragraph(p_h_text, body_style))

    story.append(Paragraph("<b>D.3 Complexity and Equivalence to BFS</b>", h2_style))
    d_analysis_text = (
        "• <b>Time Complexity:</b> With a binary min-heap, Dijkstra runs in <b>O((V + E) log V)</b> time because each vertex is extracted once (O(V log V)) and each edge relaxation invokes a heap update (O(E log V)). "
        "With a plain array scan, finding the minimum takes O(V) per vertex, yielding <b>O(V^2 + E) = O(V^2)</b> time.<br/>"
        "• <b>Equivalence to BFS:</b> If every road had length 1, Dijkstra distances <b>would exactly equal BFS hop distances</b>. "
        "When edge weights are uniform (weight = 1), the priority queue behaves like a FIFO queue where distance keys increase monotonically in integer steps, matching BFS."
    )
    story.append(Paragraph(d_analysis_text, body_style))

    # Problem E: MST
    story.append(Paragraph("6. Problem E: The Backbone (Minimum Spanning Tree)", h1_style))
    story.append(Paragraph("<b>E.1 Kruskal Algorithm Implementation with Union-Find</b>", h2_style))
    mst_intro = (
        "NorthRoute connects all 8 hubs with minimum total road length using Kruskal's algorithm. "
        "Edges are sorted by weight, and a custom Union-Find with path compression and rank prevents cycles."
    )
    story.append(Paragraph(mst_intro, body_style))

    kruskal_steps_data = [
        ["Step", "Edge Considered", "Weight", "Decision", "Union-Find Component State", "Total MST Weight"],
        ["1", "B - C", "1", "ACCEPTED", "{A}, {B, C}, {D}, {E}, {F}, {G}, {H}", "1"],
        ["2", "B - D", "2", "ACCEPTED", "{A}, {B, C, D}, {E}, {F}, {G}, {H}", "1 + 2 = 3"],
        ["3", "D - E", "2", "ACCEPTED", "{A}, {B, C, D, E}, {F}, {G}, {H}", "3 + 2 = 5"],
        ["4", "F - G", "2", "ACCEPTED", "{A}, {B, C, D, E}, {F, G}, {H}", "5 + 2 = 7"],
        ["5", "A - C", "3", "ACCEPTED", "{A, B, C, D, E}, {F, G}, {H}", "7 + 3 = 10"],
        ["6", "E - F", "3", "ACCEPTED", "{A, B, C, D, E, F, G}, {H}", "10 + 3 = 13"],
        ["7", "A - B", "4", "REJECTED", "Cycle detected (A and B already connected)", "13"],
        ["8", "C - D", "4", "REJECTED", "Cycle detected (C and D already connected)", "13"],
        ["9", "G - H", "4", "ACCEPTED", "{A, B, C, D, E, F, G, H} (All connected)", "13 + 4 = 17"]
    ]
    mst_table = Table(kruskal_steps_data, colWidths=[30, 85, 45, 65, 225, 90])
    mst_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b4f72")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (0, 0), (3, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
        ("BACKGROUND", (3, 7), (3, 8), colors.HexColor("#fadbd8")),
        ("BACKGROUND", (3, 1), (3, 6), colors.HexColor("#d5f5e3")),
        ("BACKGROUND", (3, 9), (3, 9), colors.HexColor("#d5f5e3")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(mst_table)

    story.append(Paragraph("<b>E.2 MST Analysis and Comparison (Kruskal vs Prim)</b>", h2_style))
    mst_analysis = (
        "• <b>Algorithm Chosen:</b> Kruskal's algorithm with Disjoint-Set Union.<br/>"
        "• <b>Time Complexity:</b> <b>O(E log E) = O(E log V)</b> for sorting 13 edges, followed by O(E * alpha(V)) for union-find operations.<br/>"
        "• <b>Verification:</b> Prim's algorithm was also implemented and executed, yielding the exact same total weight of <b>17</b>.<br/>"
        "• <b>When to prefer Prim over Kruskal:</b> Prim's algorithm with an adjacency matrix runs in <b>O(V^2)</b> time without needing a priority queue or edge sorting. "
        "Therefore, Prim is strongly preferred on <b>dense graphs</b> where E is close to V^2 (e.g., complete graphs), whereas Kruskal is superior on <b>sparse graphs</b> or when edges are already sorted."
    )
    story.append(Paragraph(mst_analysis, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: PROBLEM F (ANALYSIS & REASONING) & ACADEMIC INTEGRITY
    # =========================================================================
    story.append(Paragraph("7. Problem F: Analysis and Reasoning", h1_style))

    story.append(Paragraph("<b>F.1 Comprehensive Algorithm Complexity Table</b>", h2_style))
    comp_table_data = [
        ["Algorithm", "Time Complexity", "Space Complexity", "Algorithmic Technique"],
        ["0/1 Knapsack (Problem A)", "O(n * W)", "O(n * W)", "Dynamic Programming (Tabulation / Memoization)"],
        ["Coin Change (Problem B)", "O(n * T) = O(T)", "O(T)", "Dynamic Programming (Tabulation)"],
        ["BFS (Problem C)", "O(V + E)", "O(V)", "Graph Traversal (Queue-based)"],
        ["DFS (Problem C)", "O(V + E)", "O(V)", "Graph Traversal (Recursive / Stack-based)"],
        ["Dijkstra (Problem D)", "O((V + E) log V)", "O(V + E)", "Greedy / Priority Queue Traversal"],
        ["MST - Kruskal (Problem E)", "O(E log V)", "O(V + E)", "Greedy (Edge sorting + Union-Find)"],
        ["MST - Prim (Problem E)", "O((V + E) log V)", "O(V + E)", "Greedy (Cut property + Priority Queue)"]
    ]
    ct_flow = Table(comp_table_data, colWidths=[130, 115, 95, 200])
    ct_flow.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b4f72")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9f9")]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(ct_flow)

    story.append(Paragraph("<b>F.2 Greedy Heuristics versus Dynamic Programming</b>", h2_style))
    f2_text = (
        "• <b>Where Greedy Fails:</b> In Coin Change with denominations {1, 3, 4, 9} and target 6, greedy selects the largest coin 4 first, leaving remainder 2 which forces coins [4, 1, 1] (3 coins). "
        "DP finds the optimal solution [3, 3] (2 coins). Greedy fails because a locally optimal choice constrains future subproblems into suboptimal solutions.<br/>"
        "• <b>Where Greedy is Provably Correct:</b> <b>Dijkstra's algorithm</b> (with non-negative edge weights). "
        "The greedy choice selects the unvisited vertex <i>u</i> with the minimum tentative distance <i>dist[u]</i>. "
        "Because all road weights are non-negative, any alternative path from the source through another unvisited vertex must already have length >= <i>dist[u]</i>, plus additional non-negative weights. "
        "Thus, no future edge relaxation can discover a shorter path to <i>u</i>, guaranteeing that the local minimum is globally optimal."
    )
    story.append(Paragraph(f2_text, body_style))

    story.append(Paragraph("<b>F.3 Scaling Analysis: Impact of Doubling n versus Doubling W</b>", h2_style))
    f3_text = (
        "• <b>Theoretical Impact:</b> The table operations scale as <i>n * W</i>. Doubling <i>n</i> (items) increases cells to <i>2n * W</i> (factor of 2). "
        "Doubling <i>W</i> (capacity) increases cells to <i>n * 2W</i> (factor of 2).<br/>"
        "• <b>Pseudo-Polynomial Distraction:</b> Doubling <i>n</i> requires doubling the actual parcel records in input size. "
        "However, doubling <i>W</i> requires adding only a single bit to the binary representation of <i>W</i>, yet doubles the workload. "
        "If <i>W</i> scales to large values (e.g., from 18 to 18,000,000), the running time increases by a factor of 1,000,000 while the item count <i>n</i> remains just 8.<br/>"
        "• <b>Numeric Example:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- Original: n = 8, W = 18 -> 8 * 18 = 144 table cells.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- Doubling n: n = 16, W = 18 -> 16 * 18 = 288 table cells.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- Doubling W: n = 8, W = 36 -> 8 * 36 = 288 table cells."
    )
    story.append(Paragraph(f3_text, body_style))

    story.append(Paragraph("<b>F.4 Minimum Spanning Tree versus Shortest-Path Tree</b>", h2_style))
    f4_text = (
        "A Minimum Spanning Tree (MST) minimizes the <b>total global edge weight</b> necessary to connect all hubs in the network, "
        "whereas a Shortest-Path Tree (SPT) minimizes the <b>individual distance from a single source hub</b> to each other hub.<br/>"
        "• <b>Concrete Example from NorthRoute:</b> Between hubs F and H, the shortest path is the direct road F-H of length <b>5</b>. "
        "However, the MST excludes edge F-H and connects hub H via road G-H (length 4) and F-G (length 2). "
        "The MST saves 1 unit of cable globally (weight 4 instead of 5), but the route distance from F to H in the MST tree is 2 + 4 = <b>6</b>, which is longer than the direct shortest route of 5."
    )
    story.append(Paragraph(f4_text, body_style))

    # Academic Integrity and AI Use
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#1b4f72"), spaceBefore=4, spaceAfter=4))
    story.append(Paragraph("8. Academic Integrity and AI-Use Statement", h1_style))
    ai_use_text = (
        "In accordance with the course policy on academic integrity, an AI assistant was utilized to assist with code structure, "
        "formatting verification, and report drafting. All algorithm implementations, mathematical recurrences, dynamic programming tables, "
        "graph traversals, shortest-path computations, and complexity proofs were verified and calculated using personal parameters "
        "(Roll No: 24i-2013, Seed s = 13, Capacity W = 18, Target T = 43, Start Hub = F). "
        "The author has independently reviewed and verified all results through Python code execution and is prepared to explain and modify any section during oral evaluation."
    )
    story.append(Paragraph(ai_use_text, body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully: {output_filename}")


if __name__ == "__main__":
    create_report()
