# Physical Optics - Week 1: Nature of Light
## Comprehensive Study Notes

---

## 1. NATURE OF LIGHT: ELECTROMAGNETIC OSCILLATION

### 1.1 Light as Electromagnetic Waves
- Light is an electromagnetic oscillation propagating through space
- Characterized by oscillating electric (E) and magnetic (B) fields perpendicular to direction of propagation
- Both E and B fields oscillate perpendicular to each other

### 1.2 Wave Equation for Light
The wave equation for electromagnetic waves:
```
∇²E = (1/c²) ∂²E/∂t²
```
Where:
- E = Electric field vector
- c = Speed of light in medium (3 × 10⁸ m/s in vacuum)
- t = time
- ∇² = Laplacian operator (spatial second derivative)

This fundamental equation describes how electromagnetic waves propagate through space and time.

### 1.3 Electromagnetic Spectrum
The electromagnetic spectrum includes (from lowest to highest frequency):
- Radio waves (10³ Hz)
- Microwaves (10⁹ Hz)
- Infrared (10¹² Hz)
- **Visible light (10¹⁴-10¹⁵ Hz)** ← Optometry focus
- Ultraviolet (10¹⁶ Hz)
- X-rays (10¹⁸ Hz)
- Gamma rays (10²⁰ Hz)

Visible spectrum: 380 nm (violet) to 750 nm (red)

---

## 2. SINUSOIDAL OSCILLATIONS

### 2.1 Simple Harmonic Oscillation
Light can be described as simple harmonic oscillation:
```
E(x,t) = E₀ sin(kx - ωt + φ)
```

Where:
- **E₀** = Amplitude (maximum field strength)
- **k** = Wave number = 2π/λ
- **ω** = Angular frequency = 2πf
- **φ** = Phase constant
- **x** = Position
- **t** = Time

### 2.2 Transverse Nature of Light
- Light waves are **transverse waves** (oscillations perpendicular to propagation direction)
- Unlike sound waves which are longitudinal
- This transverse nature allows for **polarization** phenomena

### 2.3 Wave Properties
Light exhibits wave properties:
- Reflection
- Refraction
- Diffraction
- Interference
- Polarization

---

## 3. PARAMETERS OF LIGHT

### 3.1 Frequency (f)
- **Definition**: Number of complete oscillations per second
- **Units**: Hertz (Hz) = cycles/second
- **Range for visible light**: 4 × 10¹⁴ Hz (red) to 8 × 10¹⁴ Hz (violet)
- **Relationship**: f = c/λ
- **Constant in all media** (frequency doesn't change when light enters different medium)

### 3.2 Wavelength (λ)
- **Definition**: Distance between successive wave crests
- **Units**: Nanometers (nm), Micrometers (μm), Angstroms (Å)
- **Visible range**: 380 nm - 750 nm
- **Changes with medium**: λ_medium = λ_vacuum / n
  - Where n = refractive index of medium

**Wavelength Classification (Visible Light):**
| Color | Wavelength (nm) | Frequency (Hz) |
|-------|-----------------|----------------|
| Violet | 380-420 | 7.5-8.0 × 10¹⁴ |
| Blue | 420-490 | 6.1-7.5 × 10¹⁴ |
| Green | 490-570 | 5.3-6.1 × 10¹⁴ |
| Yellow | 570-590 | 5.1-5.3 × 10¹⁴ |
| Orange | 590-620 | 4.8-5.1 × 10¹⁴ |
| Red | 620-750 | 4.0-4.8 × 10¹⁴ |

### 3.3 Amplitude (A or E₀)
- **Definition**: Maximum displacement from equilibrium
- **Represents**: Intensity/brightness of light
- **Related to intensity**: I ∝ A²
- **Units**: V/m (electric field amplitude)

### 3.4 Phase (φ)
- **Definition**: Position of wave at reference point/time
- **Units**: Radians or degrees
- **Range**: 0 to 2π radians (0° to 360°)
- **Phase difference**: Important for interference phenomena
- **Phase velocity**: v_phase = c/n (in medium with refractive index n)

---

## 4. SOURCES OF LIGHT

### 4.1 Primary Light Sources
1. **Thermal sources**: Incandescent bulbs, sun, flames
2. **Gas discharge**: Fluorescent lamps, neon signs
3. **Light-emitting diodes (LEDs)**: Modern efficient sources
4. **Lasers**: Highly coherent light sources
5. **Bioluminescence**: Natural light production

### 4.2 Radiometry vs Photometry

#### Radiometry
- Measures total electromagnetic radiation energy
- Based on physical power of radiation
- Units: Watts (W), Joules (J)
- Accounts for all wavelengths equally
- **Not** what the eye sees

#### Photometry
- Measures visible light as perceived by human eye
- Based on luminous intensity
- Units: Candela (cd), Lumen (lm), Lux (lx)
- **Weighted** by eye's spectral sensitivity
- Eye most sensitive to green (555 nm)

### 4.3 Radiometric Units

| Quantity | Symbol | Unit | Definition |
|----------|--------|------|------------|
| Radiant Energy | Q | Joule (J) | Total energy emitted |
| Radiant Flux | Φ | Watt (W) | Power (energy/time) |
| Irradiance | E | W/m² | Flux per unit area |
| Radiant Intensity | I | W/sr | Flux per solid angle |
| Radiance | L | W/(m²·sr) | Intensity per area |

### 4.4 Photometric Units

| Quantity | Symbol | Unit | Definition |
|----------|--------|------|------------|
| Luminous Flux | Φᵥ | Lumen (lm) | Visible power |
| Luminous Intensity | Iᵥ | Candela (cd) | Visible intensity |
| Illuminance | Eᵥ | Lux (lx) | Lm/m² |
| Luminance | Lᵥ | cd/m² | Brightness/area |

---

## 5. SOLID ANGLE

### 5.1 Definition
- **Solid angle (Ω)**: 3D angle subtended by surface at point
- **Symbol**: Ω (omega)
- **Units**: Steradians (sr)
- **Range**: 0 to 4π sr (full sphere)

### 5.2 Calculation
```
Ω = A/r²
```
Where:
- A = Area of surface
- r = Distance from point to surface

### 5.3 Common Solid Angles
- Full sphere = 4π sr ≈ 12.57 sr
- Hemisphere = 2π sr
- Small cone (narrow beam) ≈ π(θ/2)² sr (for small angles)

### 5.4 Importance in Optometry
- Used in calculating light distribution from optical systems
- Important for luminous intensity calculations
- Relates to pupil size and angle of acceptance

---

## 6. LUMINOUS EFFICIENCY & EYE SENSITIVITY

### 6.1 Photopic Vision (Bright Light)
- **Wavelength of maximum sensitivity**: 555 nm (green-yellow)
- **Luminous efficiency at 555 nm**: 1.0 (defined as reference)
- **Rod saturation threshold**: ~10 cd/m² (adapts to cones)
- **Photopic vision uses**: Cone cells (color vision)
- **Color perception**: Full color vision available

**Photopic Luminous Efficiency Function (V(λ)):**
- Peaks at 555 nm
- Drops to ~0.4 at red (650 nm)
- Drops to ~0.4 at violet (460 nm)
- Nearly zero below 380 nm and above 780 nm

### 6.2 Scotopic Vision (Dim Light)
- **Wavelength of maximum sensitivity**: 507 nm (blue-green)
- **Luminous efficiency peak**: Shifted toward blue
- **Rod activation threshold**: <10⁻³ cd/m²
- **Scotopic vision uses**: Rod cells (monochromatic)
- **Color perception**: No color vision (achromatic)
- **Visual acuity**: Reduced compared to photopic

**Scotopic Luminous Efficiency Function (V'(λ)):**
- Peaks at 507 nm (blue-shifted from photopic)
- Different efficiency curve than photopic
- More sensitive to blue light
- Less sensitive to red light

### 6.3 Mesopic Vision
- **Intermediate light levels** (twilight conditions)
- **Both rods and cones** active
- **Purkinje shift**: Apparent color change with illumination
- **Luminous efficiency**: Between photopic and scotopic
- **Gradually transitions** from photopic to scotopic as light decreases

---

## 7. INVERSE SQUARE LAW OF PHOTOMETRY

### 7.1 Statement
The illuminance from a point light source varies inversely with the square of distance:

```
E = I/d²
```

Where:
- **E** = Illuminance (lux)
- **I** = Luminous intensity (candela)
- **d** = Distance from source (meters)

### 7.2 Derivation
- Light spreads uniformly in all directions (4π steradians)
- Area increases as 4πd²
- Same flux spread over larger area = lower intensity
- Therefore: I ∝ 1/d²

### 7.3 Practical Implications
- Doubling distance = 1/4 illuminance
- Tripling distance = 1/9 illuminance
- Moving light source closer is very effective (moves to power of 2)

### 7.4 Clinical Applications in Optometry
- **Slit lamp illumination**: Distance affects brightness
- **Retinal illumination**: Depends on pupil size and lamp distance
- **Examination lighting**: Proper distance for adequate illumination
- **Fundus photography**: Exposure compensation needed with distance changes

---

## 8. LAMBERT'S LAW (Cosine Law)

### 8.1 Statement
The luminous intensity in a given direction from a diffusely reflecting surface is proportional to the cosine of the angle from the normal:

```
I = I₀ cos(θ)
```

Where:
- **I** = Luminous intensity in direction θ
- **I₀** = Luminous intensity in normal direction
- **θ** = Angle from surface normal

### 8.2 Physical Meaning
- Maximum intensity perpendicular to surface (θ = 0°, cos(0) = 1)
- Intensity decreases as angle increases
- At 60° angle: I = I₀ × 0.5
- At 90° angle (parallel to surface): I = 0

### 8.3 Lambert's Cosine Law Surfaces
- **Ideal diffuse reflectors** follow Lambert's law
- Examples: Matte paper, painted walls, uniform diffuse surfaces
- **Not followed by**: Mirrors, glossy surfaces, specular reflectors

### 8.4 Luminance (Brightness)
- **Key property**: Luminance appears **constant** from all viewing angles
- **Formula**: L = I/(A cos θ)
- This is why a matte surface looks equally bright from different angles
- Specular surfaces don't follow this (mirrors appear brighter when viewed head-on)

### 8.5 Clinical Applications
- **Retinal imaging**: Understanding how light reflects from retina
- **Ophthalmoscopic examination**: Observing retinal brightness
- **Fundus photography**: Exposure considerations
- **Visual field testing**: Light stimulus presentation

---

## 9. OTHER UNITS OF LIGHT MEASUREMENT

### 9.1 Common Units in Optometry

| Unit | Symbol | Quantity Measured | Typical Use |
|------|--------|------------------|------------|
| Candela | cd | Luminous intensity | Light source strength |
| Lumen | lm | Luminous flux | Total visible light output |
| Lux | lx | Illuminance | Light falling on surface |
| Candela/m² | cd/m² | Luminance | Brightness of surface |
| Footcandle | fc | Illuminance | Light on surface (older unit) |
| Footlambert | fL | Luminance | Brightness (older unit) |

### 9.2 Conversions
- 1 lux ≈ 0.0929 footcandles
- 1 cd/m² ≈ 0.2919 footlamberts
- 1 lumen = 1 candela × 1 steradian

### 9.3 Clinical Reference Values
- **Bright sunlight**: ~100,000 lux
- **Typical office**: ~500 lux
- **Dim room**: ~50 lux
- **Scotopic threshold**: ~0.001 lux
- **Photopic threshold**: ~0.1 lux

---

## 10. RETINAL ILLUMINATION & TROLANDS

### 10.1 Retinal Illuminance
The illumination on the retina depends on:
1. **Object luminance** (brightness)
2. **Pupil diameter** (area)
3. **Eye optics** (transmission)
4. **Distance** (focal length)

### 10.2 Troland Unit
- **Definition**: Unit of retinal illumination
- **Symbol**: Td
- **Calculation**:
```
Retinal illumination (Td) = Object luminance (cd/m²) × Pupil area (mm²)
```

Where:
- Object luminance in cd/m²
- Pupil area = π(D/2)² where D = pupil diameter in mm

### 10.3 Practical Troland Values
- **Bright sunlight**: 1,000-10,000 Td
- **Typical room light**: 100-1,000 Td
- **Dim indoor light**: 10-100 Td
- **Twilight conditions**: 1-10 Td
- **Starlight**: <0.01 Td
- **Rod-cone transition**: ~10 Td

### 10.4 Importance in Optometry
- **Visual acuity testing**: Must control retinal illumination
- **Perimetry**: Light stimulus must account for pupil size
- **Fundus examination**: Brightness perceived depends on trolands
- **Contrast sensitivity**: Affected by retinal illumination level
- **Color vision testing**: Critical at specific illumination levels

### 10.5 Clinical Implications
- Dilated pupils (mydriatic): Increased retinal illumination
- Constricted pupils (miotic): Decreased retinal illumination
- Cataracts: Reduce light transmission (lower trolands for same object)
- IOL implants: Different transmission properties than natural lens

---

## 11. SUMMARY TABLE: Light Parameters

| Parameter | Symbol | Units | Key Relationship |
|-----------|--------|-------|-----------------|
| Frequency | f | Hz | f = c/λ |
| Wavelength | λ | nm | λ = c/f |
| Amplitude | A | V/m | I ∝ A² |
| Phase | φ | rad/deg | Determines interference |
| Solid Angle | Ω | sr | Ω = A/r² |
| Luminous Intensity | I | cd | I = dΦ/dΩ |
| Luminous Flux | Φ | lm | Power perceived by eye |
| Illuminance | E | lux | E = I/d² |
| Luminance | L | cd/m² | L = I/(A cos θ) |
| Retinal Illumination | - | Td | Td = L × Pupil area |

---

## 12. KEY CONCEPTS TO REMEMBER

1. **Light is electromagnetic radiation** - oscillating E and M fields
2. **Frequency is constant** - doesn't change when entering new medium
3. **Wavelength changes with medium** - λ = λ₀/n
4. **Eye sees wavelengths 380-750 nm** - peak sensitivity at 555 nm (photopic)
5. **Inverse square law** - intensity decreases with distance squared
6. **Lambert's law** - matte surfaces show constant brightness from all angles
7. **Trolands measure retinal brightness** - combination of object luminance and pupil area
8. **Photopic vs scotopic** - different sensitivities and wavelength peaks
9. **Solid angle in steradians** - measures 3D angles (0 to 4π for sphere)
10. **Radiometry vs Photometry** - physical vs perceived brightness

---

## 13. STUDY QUESTIONS

1. Why is the peak sensitivity of photopic vision at 555 nm?
2. What is the relationship between frequency and wavelength?
3. How does the inverse square law apply to slit lamp illumination?
4. Explain why luminance appears constant from different viewing angles for matte surfaces.
5. What is the difference between illuminance and luminance?
6. How would a cataract affect retinal illumination in trolands?
7. Why is the scotopic peak wavelength different from photopic?
8. Calculate the illuminance at 2 meters from a 1000 candela light source.
9. What factors affect the troland value on the retina?
10. How does pupil size affect retinal illumination?

---

**Textbook Reference:**
Principles of Physical Optics by Charles A. Bennett (2nd Edition)
- Chapter 1: Nature and Propagation of Light
- Chapter 2: Radiometry and Photometry

**Additional Resources:**
- ISO 23601 - Light and Lighting - Measurement and Calculation
- CIE (International Commission on Illumination) Standards
- Basic Optics textbooks for wave mechanics review

---

*Last Updated: 2026*
*Course: Physical Optics - Week 1*
